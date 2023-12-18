oad_copy = list(self.road)  # Buat salinan baru dari self.road
                wall_copy = list(self.walls)  # Buat salinan baru dari self.walls
                
                # Periksa elemen-elemen individual, bukan seluruh list
                possible_goals = [value for value in road_copy if value not in wall_copy and value not in self.orbs and value != self.player_pos and value != self.enemy_pos]
                
                if possible_goals:
                    random_value = random.choice(possible_goals)
                    print(random_value)
                    self.goal_pos = random_value
                    print(self.goal_pos[0], self.goal_pos[1])
                    self.road.remove(random_value)