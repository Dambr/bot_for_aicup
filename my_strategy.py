import model
# import Target_Weapon

# бежим к первому "лучшему" оружию
# непрерывно стреляем -> учим стрелять только когда он видит цель
# бежим к противнику
# постоянно прыгаем


class MyStrategy:
	def __init__(self):
		self.boo = True
		self.swap_weapon = True
		self.jump = True
		self.jump_down = False
		self.best_weapon = 'ASSAULT_RIFLE'
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


		# Текущая целевая точка
		self.target_pos = unit.position

		nearest_enemy = min(
			filter(lambda u: u.player_id != unit.player_id, game.units),
			key=lambda u: distance_sqr(u.position, unit.position),
			default=None)


		nearest_weapon = getNearestWeapon(self.best_weapon)
		
		self.target_pos = nearest_weapon.position

		if unit.weapon and str(unit.weapon.typ) == 'WeaponType.' + self.best_weapon:
			self.swap_weapon = False
			self.target_pos = nearest_enemy.position

		

		if self.target_pos.y >= unit.position.x:
			self.jump = True
		else:
			self.jump = False

		









		
		debug.draw(model.CustomData.Log("Unit pos: {0}:{1}".format( unit.position.x, unit.position.y )))
		debug.draw(model.CustomData.Log("Weapon pos: {0}:{1}".format( nearest_weapon.position.x, nearest_weapon.position.y )))
		
		
		
		aim = model.Vec2Double(0, 0)
		if nearest_enemy is not None:
			aim = model.Vec2Double(
				nearest_enemy.position.x - unit.position.x,
				nearest_enemy.position.y - unit.position.y)
		jump = self.target_pos.y > unit.position.y
		if self.target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
			self.jump = True
		if self.target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
			self.jump = True


		return model.UnitAction(
			velocity = (self.target_pos.x - unit.position.x) * game.properties.unit_max_horizontal_speed,
			# jump = jump,
			jump = self.jump,
			jump_down = not jump,
			aim = aim,
			shoot = True,
			swap_weapon = self.swap_weapon,
			plant_mine = True)

if __name__ == "__main__":
	c = MyStrategy()
