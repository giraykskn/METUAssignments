#include <stdio.h>
#include <iostream>
#include <sys/socket.h>
#include "message.h"
#include "logging.h"
#include <string>
#include <unistd.h>
#include <sys/wait.h>
#define PIPE(fd) socketpair(AF_UNIX, SOCK_STREAM, PF_UNIX, fd)

int abs(int x) {
  if(x < 0)
    return -x;
  else
    return x;
}

int main(int argc, char *argv[]) {
  int health, damage, defence, range;
  health = atoi(argv[1]);
  damage = atoi(argv[2]);
  defence = atoi(argv[3]);
  range = atoi(argv[4]);

  //fprintf(stderr, "%i %i %i %i\n",health, damage, defence, range);

  monster_response mr;
  mr.mr_type = mr_ready;
  mr.mr_content.move_to.x = 0;
  mr.mr_content.move_to.y = 0;
  mr.mr_content.attack = 0;
  write(1, &mr, sizeof(monster_response));

  while (true) {
      monster_message mm;
      read(0, &mm, sizeof(monster_message));
      if (mm.game_over) {
        break;
      }
      int realDamage = mm.damage - defence;
      if(realDamage < 0) {
        realDamage = 0;
      }
      health -= realDamage;
      //fprintf(stderr, "%i\n",realDamage);
      int distance = abs(mm.new_position.x - mm.player_coordinate.x) + abs(mm.new_position.y - mm.player_coordinate.y);
      //fprintf(stderr, "Player = %i %i , Monster = %i %i ;Distance is %i, range is %i\n",mm.player_coordinate.x, mm.player_coordinate.y, mm.new_position.x, mm.new_position.y, distance, range);
      monster_response mr;
      if (health <= 0) {
        mr.mr_type = mr_dead;
        write(1, &mr, sizeof(monster_response));
        break;
      }
      else if(distance <= range) {
        mr.mr_type = mr_attack;
        mr.mr_content.attack = damage;
        //fprintf(stderr, "Hit player by %i\n",damage);
        write(1, &mr, sizeof(monster_response));
      }
      else{
        mr.mr_type = mr_move;
        int distances[8];
        coordinate moveTo;
        distances[0] = abs(mm.new_position.x - mm.player_coordinate.x) + abs(mm.new_position.y - 1 - mm.player_coordinate.y);
        distances[1] = abs(mm.new_position.x + 1 - mm.player_coordinate.x) + abs(mm.new_position.y - 1 - mm.player_coordinate.y);
        distances[2] = abs(mm.new_position.x + 1 - mm.player_coordinate.x) + abs(mm.new_position.y - mm.player_coordinate.y);
        distances[3] = abs(mm.new_position.x + 1 - mm.player_coordinate.x) + abs(mm.new_position.y + 1 - mm.player_coordinate.y);
        distances[4] = abs(mm.new_position.x - mm.player_coordinate.x) + abs(mm.new_position.y + 1 - mm.player_coordinate.y);
        distances[5] = abs(mm.new_position.x - 1 - mm.player_coordinate.x) + abs(mm.new_position.y + 1 - mm.player_coordinate.y);
        distances[6] = abs(mm.new_position.x - 1 - mm.player_coordinate.x) + abs(mm.new_position.y - mm.player_coordinate.y);
        distances[7] = abs(mm.new_position.x - 1 - mm.player_coordinate.x) + abs(mm.new_position.y - 1 - mm.player_coordinate.y);
        int bestDistance = 9999;
        int best = -1;
        for(int i = 0; i < 8; i++) {
          if (distances[i] < bestDistance) {
            best = i;
            bestDistance = distances[i];
          }
        }
        switch (best) {
          case 0:
            moveTo.x = mm.new_position.x; moveTo.y = mm.new_position.y - 1;
            break;
          case 1:
            moveTo.x = mm.new_position.x + 1; moveTo.y = mm.new_position.y - 1;
            break;
          case 2:
            moveTo.x = mm.new_position.x + 1; moveTo.y = mm.new_position.y;
            break;
          case 3:
            moveTo.x = mm.new_position.x + 1; moveTo.y = mm.new_position.y + 1;
            break;
          case 4:
            moveTo.x = mm.new_position.x; moveTo.y = mm.new_position.y + 1;
            break;
          case 5:
            moveTo.x = mm.new_position.x - 1; moveTo.y = mm.new_position.y + 1;
            break;
          case 6:
            moveTo.x = mm.new_position.x - 1; moveTo.y = mm.new_position.y;
            break;
          case 7:
            moveTo.x = mm.new_position.x - 1; moveTo.y = mm.new_position.y - 1;
            break;
        }
        mr.mr_content.move_to = moveTo;
        write(1, &mr, sizeof(monster_response));
      }

  }
  exit(0);

}
