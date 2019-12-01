import model
import math
# import Target_Weapon

# бежим к первому "лучшему" оружию
# непрерывно стреляем -> учим стрелять только когда он видит цель
# бежим к противнику
# постоянно прыгаем
# навесить обработчик, что если в руках рокетница и рядом непустые тайлы, то не стрелять

# просчитать движение к заданному объекту !!!!

class MyStrategy:
	def __init__(self):
		self.boo = True
		self.index = 1 # Хватаем ROCKET_LAUNCHER
		self.count_of_bad_ticks = 0
		self.velocity = 0
		self.swap_weapon = True
		self.jump = True
		self.jump_down = False

		self.shoot = False
		self.best_weapon = ['ASSAULT_RIFLE', 'ROCKET_LAUNCHER', 'PISTOL'] # 'ASSAULT_RIFLE'
		self.damage_radius = 0
		pass

	

	def get_action(self, unit, game, debug):
		

		# Replace this code with your own
		def distance_sqr(a, b):
			return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

		def getNearestWeapon(weapon_name):
			nearest_weapon = min(
				filter(lambda box: isinstance(
					box.item, model.Item.Weapon), game.loot_boxes),
				key=lambda box: distance_sqr(box.position, unit.position) if str(box).split('WeaponType.')[1].split(':')[0] == weapon_name else len(game.level.tiles[0]) * 2, # если интересующее нас оружие, кладем его координату, иначе кладем координату заведомо проигрышную, ширина поля *
				default=None)
			return nearest_weapon
		def getNearestHealthPack():
			nearest_healthPack = min(
				filter(lambda box: isinstance(
					box.item, model.Item.HealthPack), game.loot_boxes),
				key=lambda box: distance_sqr(box.position, unit.position),
				default=None)
			return nearest_healthPack


		def getBooleanShoot():
			# заменить позицию на упрежденную точку, в которой будет персонаж, когда он будет с выстрелом на заданном расстоянии
			koords = list()
			tan = ( max(nearest_enemy.position.y, unit.position.y) - min(nearest_enemy.position.y, unit.position.y)) / (max(nearest_enemy.position.x, unit.position.x) - min(nearest_enemy.position.x, unit.position.x) )
			debug.draw(model.CustomData.Log("tan: {0}".format( tan )))
			# for i in range(min(int(unit.position.x), int(nearest_enemy.position.x)), max(int(unit.position.x), int(nearest_enemy.position.x))):
			# 	koords.append([i, int(i * tan)])
			for i in range(min(int(unit.position.x), int(nearest_enemy.position.x)), max(int(unit.position.x), int(nearest_enemy.position.x))):
				# Кладем в массив пару: координата x и y
				koords.append([i, min(int(nearest_enemy.position.y), int(unit.position.y)) + int(i * tan)])
			
			result = False
			if len(koords) == 0:
				result = True
			else:
				try:
					for koord in koords:
						if game.level.tiles[koord[0]][koord[1]] == model.Tile.WALL:
							result = False
							break
					else:
						result = True
				except:
					result = True

			return result


		# Текущая целевая точка
		self.target_pos = unit.position

		nearest_enemy = min(
			filter(lambda u: u.player_id != unit.player_id, game.units),
			key=lambda u: distance_sqr(u.position, unit.position),
			default=None)


		nearest_weapon = getNearestWeapon(self.best_weapon[self.index % 3])
		nearest_healthPack = getNearestHealthPack()
		self.target_pos = nearest_weapon.position

		

		# Если подобрано лучшее оружее, то больше пушки не меняем
		if (unit.weapon and str(unit.weapon.typ) == 'WeaponType.' + self.best_weapon[self.index % 3]) or self.shoot:
			self.swap_weapon = False
			self.target_pos = nearest_weapon.position

		# Если пушка подобрана, то определяем, стрелять или нет
		if unit.weapon:
			
			if self.target_pos.y > unit.position.y:
				if self.target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y + 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] != model.Tile.WALL and game.level.tiles[int(unit.position.x)][int(unit.position.y + 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] != model.Tile.WALL:
					self.shoot = getBooleanShoot()
				elif self.target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y + 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] != model.Tile.WALL and game.level.tiles[int(unit.position.x)][int(unit.position.y + 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] != model.Tile.WALL:
					self.shoot = getBooleanShoot()
			else:
				if self.target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y - 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] != model.Tile.WALL and game.level.tiles[int(unit.position.x)][int(unit.position.y)] != model.Tile.WALL and game.level.tiles[int(unit.position.x)][int(unit.position.y - 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y - 1)] != model.Tile.WALL:
					self.shoot = getBooleanShoot()
				elif self.target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y - 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] != model.Tile.WALL and game.level.tiles[int(unit.position.x)][int(unit.position.y)] != model.Tile.WALL and game.level.tiles[int(unit.position.x)][int(unit.position.y - 1)] != model.Tile.WALL and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y - 1)] != model.Tile.WALL:
					self.shoot = getBooleanShoot()
			if int(math.sqrt(distance_sqr(unit.position, nearest_enemy.position))) < 1:
				self.shoot = True
			debug.draw(model.CustomData.Log("Shoot: {0}".format( self.shoot )))

			if (self.shoot and unit.health == game.properties.unit_max_health) or (self.shoot and unit.health < game.properties.unit_max_health and not nearest_healthPack):
				self.target_pos = unit.position
				self.jump = False
				self.jump_down = False
			else:
				self.target_pos = nearest_enemy.position

			
		else:
			self.target_pos = nearest_weapon.position

		

		# Если уровень здоровья не 100%, бежим к ближайшей аптечке
		if unit.health < game.properties.unit_max_health and not unit.weapon:
			try:
				self.target_pos = nearest_healthPack.position
			except:
				self.target_pos = nearest_weapon.position
		elif unit.health < game.properties.unit_max_health and unit.weapon:
			try:
				self.target_pos = nearest_healthPack.position
			except:
				self.target_pos = nearest_enemy.position



		# Если цель выше нас или на одном уровне с нами, то прыгаем
		# self.jump = self.target_pos.y >= unit.position.y
		# Так же прыгаем, если тайл мешает пройти
		if self.target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
			self.jump = True
			self.jump_down = False
		if self.target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
			self.jump = True
			self.jump_down = False

		if int(self.target_pos.x) == int(unit.position.x) and int(self.target_pos.y) < int(unit.position.y):
			self.jump = False
			self.jump_down = True
		
		# Если противник мешает пройти, пытаемся его перепрыгнуть
		if self.target_pos != nearest_enemy.position and math.fabs(nearest_enemy.position.x - unit.position.x) < 1:
			self.jump = True
			self.jump_down = True

		
		
		# if self.boo:
		# 	print(unit.health)	
		# 	self.boo = False
		# Стараемся держаться на "безопасном расстоянии от врага"
		if self.target_pos == unit.position and nearest_enemy.position.x < unit.position.x:
			self.target_pos.x = self.target_pos.x + 5
		elif self.target_pos == unit.position and nearest_enemy.position.x > unit.position.x:
			self.target_pos.x = self.target_pos.x - 5



		
		
		debug.draw(model.CustomData.Log("Speed: {0}".format( math.fabs(int((self.target_pos.x - unit.position.x))) * game.properties.unit_max_horizontal_speed )))
		debug.draw(model.CustomData.Log("Target: {0}:{1}".format( int(self.target_pos.x - unit.position.x), int(self.target_pos.y - unit.position.y) )))
		

		# Прицеливание бота
		# if self.boo:

		# 	# main()
		# 	self.boo = False
		
		
		
		aim = model.Vec2Double(0, 0)
		

		if nearest_enemy is not None:
			aim = model.Vec2Double(
				nearest_enemy.position.x - unit.position.x,
				nearest_enemy.position.y - unit.position.y)
		
		# # Если цель выше нас или на одном уровне с нами, то прыгаем
		# self.jump = self.target_pos.y >= unit.position.y
		# # Так же прыгаем, если тайл мешает пройти
		# if self.target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
		# 	self.jump = True
		# if self.target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
		# 	self.jump = True


		return model.UnitAction(
			# velocity = (self.target_pos.x - unit.position.x) * game.properties.unit_max_horizontal_speed,
			velocity = (self.target_pos.x - unit.position.x) * game.properties.unit_max_horizontal_speed,
			jump = self.jump,
			jump_down = self.jump_down,
			aim = aim,
			shoot = self.shoot,
			swap_weapon = self.swap_weapon,
			plant_mine = False)


