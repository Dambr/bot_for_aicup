import model
import math
# import Target_Weapon

# бежим к первому "лучшему" оружию
# непрерывно стреляем -> учим стрелять только когда он видит цель
# бежим к противнику
# постоянно прыгаем
# навесить обработчик, что если в руках рокетница и рядом непустые тайлы, то не стрелять

class MyStrategy:
	def __init__(self):
		self.boo = True
		self.swap_weapon = True
		self.jump = True
		self.jump_down = False

		self.shoot = False
		self.best_weapon = 'ROCKET_LAUNCHER' # 'ASSAULT_RIFLE'
		pass

	

	def get_action(self, unit, game, debug):
		# Replace this code with your own
		def distance_sqr(a, b):
			return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

		def getNearestWeapon(weapon_name):
			nearest_weapon = min(
				filter(lambda box: isinstance(
					box.item, model.Item.Weapon), game.loot_boxes),
				key=lambda box: distance_sqr(box.position, unit.position) if str(box).split('WeaponType.')[1].split(':')[0] == weapon_name else len(game.level.tiles) * 2,
				default=None)
			return nearest_weapon

		def getBooleanShoot():

			if nearest_enemy.position.x > unit.position.x + 1:
				if str(unit.weapon.typ) == 'WeaponType.' + 'ROCKET_LAUNCHER' and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
					return False
			elif nearest_enemy.position.x < unit.position.x - 1:
				if str(unit.weapon.typ) == 'WeaponType.' + 'ROCKET_LAUNCHER' and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
					return False

			koords = list()
			tan = ( max(nearest_enemy.position.y, unit.position.y) - min(nearest_enemy.position.y, unit.position.y)) / (max(nearest_enemy.position.x, unit.position.x) - min(nearest_enemy.position.x, unit.position.x) )

			for i in range(min(int(unit.position.x), int(nearest_enemy.position.x)), max(int(unit.position.x), int(nearest_enemy.position.x))):
				koords.append([i, int(i * tan)])
			
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


		nearest_weapon = getNearestWeapon(self.best_weapon)
		
		self.target_pos = nearest_weapon.position


		# Если подобрано лучшее оружее, то больше пушки не меняем
		if unit.weapon and str(unit.weapon.typ) == 'WeaponType.' + self.best_weapon:
			self.swap_weapon = False
			self.target_pos = nearest_enemy.position

		if unit.weapon:
			self.shoot = getBooleanShoot()









		
		debug.draw(model.CustomData.Log("Unit pos: {0}:{1}".format( unit.position.x, unit.position.y )))
		

		# Прицеливание бота
		if self.boo:

			self.boo = False
		
		
		
		aim = model.Vec2Double(0, 0)
		

		if nearest_enemy is not None:
			aim = model.Vec2Double(
				nearest_enemy.position.x - unit.position.x,
				nearest_enemy.position.y - unit.position.y)
		
		# Если цель выше нас или на одном уровне с нами, то прыгаем
		self.jump = self.target_pos.y >= unit.position.y
		# Так же прыгаем, если тайл мешает пройти
		if self.target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
			self.jump = True
		if self.target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
			self.jump = True


		return model.UnitAction(
			velocity = (self.target_pos.x - unit.position.x) * game.properties.unit_max_horizontal_speed,
			jump = self.jump,
			jump_down = not self.jump,
			aim = aim,
			shoot = self.shoot,
			swap_weapon = self.swap_weapon,
			plant_mine = True)


