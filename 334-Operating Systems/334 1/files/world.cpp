#include <stdio.h>
#include <iostream>
#include <sys/socket.h>
#include "message.h"
#include "logging.h"
#include <string>
#include <unistd.h>
#include <sys/wait.h>
#define PIPE(fd) socketpair(AF_UNIX, SOCK_STREAM, PF_UNIX, fd)

struct monster {
  char exec[1024];
  char name;
  coordinate pos;
  char health[1024];
  char damage[1024];
  char defence[1024];
  char range[1024];
};

void prepareMonsterCoordinates(coordinate monsterCoordinates[], int monsterPositions[], monster* monsters, bool* isMonsterAlive, int noOfMonsters, int aliveMonsterAmount) {
  int cur = 0;
  for(int i = 0; i < noOfMonsters; i++) {
    if(isMonsterAlive[i]) {
      monsterCoordinates[cur] = monsters[i].pos;
      monsterPositions[cur] = i;
      cur++;
    }
  }
  for(int i = 0; i < aliveMonsterAmount; i++) {
    for(int j = i + 1; j < aliveMonsterAmount; j++) {
      if(monsterCoordinates[i].x > monsterCoordinates[j].x) {
        coordinate tmp = monsterCoordinates[i];
        monsterCoordinates[i] = monsterCoordinates[j];
        monsterCoordinates[j] = tmp;
        int tmp2 = monsterPositions[i];
        monsterPositions[i] = monsterPositions[j];
        monsterPositions[j] = tmp2;
      }
      else if(monsterCoordinates[i].x == monsterCoordinates[j].x) {
        if(monsterCoordinates[i].y > monsterCoordinates[j].y) {
          coordinate tmp = monsterCoordinates[i];
          monsterCoordinates[i] = monsterCoordinates[j];
          monsterCoordinates[j] = tmp;
          int tmp2 = monsterPositions[i];
          monsterPositions[i] = monsterPositions[j];
          monsterPositions[j] = tmp2;
        }
      }
    }
  }
}

void mapHandler(map_info &m, int widthOfRoom, int heightOfRoom, coordinate doorPos, coordinate playerPos, int aliveMonsterAmount, monster monsters[], int monsterPositions[]) {
  m.map_width = widthOfRoom;
  m.map_height = heightOfRoom;
  m.door = doorPos;
  m.player = playerPos;
  m.alive_monster_count = aliveMonsterAmount;
  for(int i = 0; i < aliveMonsterAmount; i++) {
    m.monster_types[i] = monsters[monsterPositions[i]].name;
    m.monster_coordinates[i] = monsters[monsterPositions[i]].pos;
  }
}

int main() {
  int widthOfRoom, heightOfRoom;
  int xOfPlayer, yOfPlayer;
  char execOfPlayer[1024];
  char playerArgs1[1024], playerArgs2[1024], playerArgs3[1024], playerArgs4[1024], playerArgs5[1024];
  int noOfMonsters;
  monster* monsters;
  pid_t* pids;
  int* fds;
  bool isGameRunning = true;
  bool* isMonsterAlive;
  bool isPlayerAlive;
  bool reachedDoor;
  coordinate doorPos;

  //player message variables
  coordinate playerPos;
  int playerDamageTaken;
  int aliveMonsterAmount;
  int newAliveMonsterAmount;
  coordinate monsterCoordinates[MONSTER_LIMIT];
  int monsterPositions[MONSTER_LIMIT];

  map_info m;
  game_over_status go;

  scanf("%i %i", &widthOfRoom, &heightOfRoom);
  scanf("%s %s", playerArgs1, playerArgs2);
  scanf("%i %i", &xOfPlayer, &yOfPlayer);
  scanf("%s %s %s %s", execOfPlayer, playerArgs3, playerArgs4, playerArgs5);
  scanf("%i", &noOfMonsters);
  doorPos.x = atoi(playerArgs1);
  doorPos.y = atoi(playerArgs2);
  monsters = new monster[noOfMonsters];
  pids = new pid_t[noOfMonsters+1];
  fds = new int[noOfMonsters+1];
  char* playerArgs[7] = {execOfPlayer, playerArgs1, playerArgs2, playerArgs3, playerArgs4, playerArgs5, NULL};
  for(int i = 0; i<noOfMonsters;i++) {
    char name[2];
    scanf("%s %s %i %i %s %s %s %s", monsters[i].exec, name, &monsters[i].pos.x, &monsters[i].pos.y, monsters[i].health, monsters[i].damage, monsters[i].defence, monsters[i].range);
    monsters[i].name = name[0];
  }

  //initalize some variables
  playerPos.x = xOfPlayer;
  playerPos.y = yOfPlayer;
  aliveMonsterAmount = noOfMonsters;

  int fd[2];
  PIPE(fd);
  if((pids[0] = fork()) > 0) { //Parent
    close(fd[1]);
    fds[0] = fd[0];
  }
  else {
    close(fd[0]);
    dup2(fd[1],0);
    dup2(fd[1],1);
    close(fd[1]);
    execvp(execOfPlayer,playerArgs);
  }

  for(int i=0; i<noOfMonsters; i++) {
    int fd[2];
    PIPE(fd);
    if((pids[i+1] = fork()) > 0) { //Parent
      close(fd[1]);
      fds[i+1] = fd[0];
    }
    else {
      close(fd[0]);
      dup2(fd[1],0);
      dup2(fd[1],1);
      close(fd[1]);
      char* monsterArgs[6] = {monsters[i].exec, monsters[i].health, monsters[i].damage, monsters[i].defence, monsters[i].range, NULL};
      //fprintf(stderr, "%s %s %s %s\n", monsterArgs[1], monsterArgs[2], monsterArgs[3], monsterArgs[4]);
      execvp(monsters[i].exec, monsterArgs);
    }
  }

  player_response playerFirstResponse;
  read(fds[0], &playerFirstResponse, sizeof(player_response));
  monster_response monsterFirstResponses[MONSTER_LIMIT];
  for(int i = 0; i < noOfMonsters; i++) {
    read(fds[i+1], &monsterFirstResponses[i], sizeof(monster_response));
  }
  if(playerFirstResponse.pr_type != pr_ready) {
    //std::cout << "Player not ready!" << std::endl;
    return 0;
  }
  for(int i = 0;i < noOfMonsters; i++) {
    if(monsterFirstResponses[i].mr_type != mr_ready) {
      //std::cout << "Monster " << i << " not ready!" << std::endl;
      return 0;
    }
  }
  //std::cout << "Everyone is ready!" << std::endl;
  isPlayerAlive = true;
  reachedDoor = false;
  isMonsterAlive = new bool[noOfMonsters];
  for(int i = 0; i < noOfMonsters; i++) {
    isMonsterAlive[i] = true;
  }
  prepareMonsterCoordinates(monsterCoordinates, monsterPositions, monsters, isMonsterAlive, noOfMonsters, aliveMonsterAmount);
  mapHandler(m, widthOfRoom, heightOfRoom, doorPos, playerPos, aliveMonsterAmount, monsters, monsterPositions);
  print_map(&m);
  playerDamageTaken = 0;
  int turnNo = 0;
  while(isGameRunning) {


    turnNo++;
    //std::cout << "Turn: " << turnNo << std::endl;
    player_response pr;
    monster_message mm[MONSTER_LIMIT];
    for(int i = 0; i < aliveMonsterAmount; i++) {
      mm[monsterPositions[i]].damage = 0;
    }




    //PLAYER PART -------------------------------------------------------------------------------------------------------
    //std::cout << playerDamageTaken << std::endl;
    player_message pm;
    pm.new_position = playerPos;
    pm.total_damage = playerDamageTaken;
    pm.alive_monster_count = aliveMonsterAmount;
    for(int i = 0; i < MONSTER_LIMIT; i++) {
        pm.monster_coordinates[i] = monsterCoordinates[i];
    }
    pm.game_over = !isGameRunning;
    //std::cout << "Write player" << std::endl;
    write(fds[0], &pm, sizeof(player_message));
    //std::cout << "Read player" << std::endl;
    int playerReadSize = read(fds[0], &pr, sizeof(player_response));
    if(playerReadSize == 0) {
      //std::cout << "Player left!" << std::endl;
      go = go_left;
      break;
    }
    bool canMove = true;
    switch(pr.pr_type) {
      case pr_move:
        for(int i = 0; i < aliveMonsterAmount; i++) {
          if(monsterCoordinates[i].x == pr.pr_content.move_to.x && monsterCoordinates[i].y == pr.pr_content.move_to.y  && isMonsterAlive[monsterPositions[i]]) {
            canMove = false;
          }
        }
        if(pr.pr_content.move_to.x != doorPos.x  || pr.pr_content.move_to.y != doorPos.y) {
          if(pr.pr_content.move_to.x <= 0 || pr.pr_content.move_to.x > widthOfRoom - 2) {
            canMove = false;
          }
          if(pr.pr_content.move_to.y <= 0 || pr.pr_content.move_to.y > heightOfRoom - 2) {
            canMove = false;
          }
        }
        if(canMove) {
          playerPos = pr.pr_content.move_to;
          //std::cout << "Player moved to: " << playerPos.x << " " << playerPos.y << std::endl;
          if(playerPos.x == doorPos.x && playerPos.y == doorPos.y) {
            reachedDoor = true;
          }
        }
        break;
      case pr_attack:
        for(int i = 0; i < aliveMonsterAmount; i++) {
          if(pr.pr_content.attacked[i] > 0) {
            mm[monsterPositions[i]].damage = pr.pr_content.attacked[i];
            //std::cout << "Player attacked monster: " << monsters[monsterPositions[i]].pos.x << " " << monsters[monsterPositions[i]].pos.y << std::endl;
          }
        }
        break;
      case pr_dead:
        isPlayerAlive = false;
        break;
    }
    if(!isPlayerAlive) {
      //std::cout << "Player dead recieved!" << std::endl;
      go = go_died;
      break;
    }
    if(reachedDoor) {
      //std::cout << "Player moved to door!" << std::endl;
      go = go_reached;
      break;
    }
    playerDamageTaken = 0;
    //Player Done-------------------------------------------------------------------------------------------------------------------



    //std::cout << "Player position sent: " << playerPos.x << " " << playerPos.y << std::endl;
    for(int i = 0; i < aliveMonsterAmount; i++) {
      mm[monsterPositions[i]].new_position = monsters[monsterPositions[i]].pos;
      mm[monsterPositions[i]].player_coordinate = playerPos;
      mm[monsterPositions[i]].game_over = !isGameRunning;
      //std::cout << "Write monster " << i << std::endl;
      write(fds[monsterPositions[i]+1], &mm[monsterPositions[i]], sizeof(monster_message));
    }
    newAliveMonsterAmount = aliveMonsterAmount;
    for(int i = 0; i < aliveMonsterAmount; i++) {
      bool canMove = true;
      monster_response mr;
      //std::cout << "Read monster " << i << std::endl;
      read(fds[monsterPositions[i]+1], &mr, sizeof(monster_response));
      //std::cout << "Monster at " << monsters[monsterPositions[i]].pos.x << " " << monsters[monsterPositions[i]].pos.y << std::endl;
      switch(mr.mr_type) {
        case mr_move:
          if(mr.mr_content.move_to.x == playerPos.x && mr.mr_content.move_to.y == playerPos.y) {
            canMove = false;
          }
          for(int j = 0; j < aliveMonsterAmount; j++) {
            if(i != j && mr.mr_content.move_to.x == monsters[monsterPositions[j]].pos.x && mr.mr_content.move_to.y == monsters[monsterPositions[j]].pos.y && isMonsterAlive[monsterPositions[j]]) {
              canMove = false;
            }
          }
          if(mr.mr_content.move_to.x <= 0 || mr.mr_content.move_to.x > widthOfRoom - 2) {
            canMove = false;
          }
          if(mr.mr_content.move_to.y <= 0 || mr.mr_content.move_to.y > heightOfRoom - 2) {
            canMove = false;
          }
          if(canMove) {
            //std::cout << "Monster moved from " << monsters[monsterPositions[i]].pos.x << " " << monsters[monsterPositions[i]].pos.y << " to " << mr.mr_content.move_to.x << " " << mr.mr_content.move_to.y << std::endl;
            monsters[monsterPositions[i]].pos = mr.mr_content.move_to;
          }
          break;
        case mr_attack:
          //std::cout << "Monster attacked by " << mr.mr_content.attack << std::endl;
          playerDamageTaken += mr.mr_content.attack;
          break;
        case mr_dead:
          //std::cout << "Monster at " << i << " dead" << std::endl;
          isMonsterAlive[monsterPositions[i]] = false;
          newAliveMonsterAmount--;
          int s;
          close(fds[monsterPositions[i]+1]);
          waitpid(pids[monsterPositions[i]+1], &s, 0);
          //prepareMonsterCoordinates(monsterCoordinates, monsterPositions, monsters, isMonsterAlive, noOfMonsters, aliveMonsterAmount);
          break;
      }
    }
    aliveMonsterAmount = newAliveMonsterAmount;
    if(aliveMonsterAmount == 0) {
      //std::cout << "No monsters alive!" << std::endl;
      go = go_survived;
      break;
    }
    prepareMonsterCoordinates(monsterCoordinates, monsterPositions, monsters, isMonsterAlive, noOfMonsters, newAliveMonsterAmount);
    mapHandler(m, widthOfRoom, heightOfRoom, doorPos, playerPos, newAliveMonsterAmount, monsters, monsterPositions);
    print_map(&m);
  }
  prepareMonsterCoordinates(monsterCoordinates, monsterPositions, monsters, isMonsterAlive, noOfMonsters, aliveMonsterAmount);
  mapHandler(m, widthOfRoom, heightOfRoom, doorPos, playerPos, aliveMonsterAmount, monsters, monsterPositions);
  print_map(&m);
  print_game_over(go);
  if(go != go_left) {
    int s;
    player_message pdead;
    pdead.game_over = true;
    write(fds[0], &pdead, sizeof(player_message));
    close(fds[0]);
    waitpid(pids[0], &s, 0);
  }  
  for(int i = 0; i < noOfMonsters; i++) {
    if(isMonsterAlive[i]) {
      monster_message mdead;
      mdead.game_over = true;
      write(fds[i+1], &mdead, sizeof(monster_message));
      int s;
      close(fds[i+1]);
      waitpid(pids[i+1], &s, 0);
    }
  }
  return 0;
}
