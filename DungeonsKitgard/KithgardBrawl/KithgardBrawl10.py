enemy_types = {}
enemy_types['shaman'] = {'danger': 10, 'focus': 50}
enemy_types['warlock'] = {'danger': 10, 'focus': 30}
enemy_types['arrow-tower'] = {'danger': 10, 'focus': 20}
enemy_types['catapult'] = {'danger': 10, 'focus': 100}
enemy_types['artillery'] = {'danger': 10, 'focus': 100}
enemy_types['witch'] = {'danger': 8, 'focus': 50}
enemy_types['brawler'] = {'danger': 7, 'focus': 55}
enemy_types['ogre'] = {'danger': 5, 'focus': 40}
enemy_types['chieftain'] = {'danger': 6, 'focus': 35}
enemy_types['thrower'] = {'danger': 3, 'focus': 22}
enemy_types['munchkin'] = {'danger': 2, 'focus': 15}
enemy_types['yak'] = {'danger': -1, 'focus': 0}
enemy_types['ice-yak'] = {'danger': -1, 'focus': 0}


def findTarget():
    danger = 0
    enemy_return = None
    for type in enemy_types.keys():
        if enemy_types[type].danger > danger:
            enemy = hero.findNearest(hero.findByType(type))
            if enemy and hero.distanceTo(enemy) < enemy_types[type].focus:
                enemy_return = enemy
                danger = enemy_types[type].danger
    if danger < 3:
        enemy_return = None
    return enemy_return


def pickUpNearestItem(items):
    nearestItem = hero.findNearest(items)
    if nearestItem:
        moveTo(nearestItem.pos)


def moveTo(position, fast=True):
    if (hero.isReady("jump") and hero.distanceTo(position) > 10 and fast):
        hero.jumpTo(position)
    else:
        hero.move(position)


def attack(target):
    if target:
        if (hero.distanceTo(target) > 10):
            moveTo(target.pos)
        elif (hero.isReady("bash")):
            hero.bash(target)
        elif (hero.canCast('chain-lightning', target)):
            hero.cast('chain-lightning', target)
        elif (hero.isReady("attack")):
            hero.attack(target)
        else:
            hero.shield()


summonTypes = ['soldier']


def summonTroops():
    type = summonTypes[len(hero.built) % len(summonTypes)]
    if hero.gold > hero.costOf(type):
        hero.summon(type)


def commandTroops():
    for index, friend in enumerate(hero.findFriends()):
        if friend.type == 'archer':
            CommandArcher(friend)
        elif friend.type == 'paladin':
            CommandPaladin(friend)
        elif friend.type == 'soldier':
            CommandSoldier(friend)
        elif friend.type == 'peasant':
            CommandPeasant(friend)


def CommandPaladin(paladin):
    if (paladin.canCast("heal") and hero.health < hero.maxHealth * 0.6):
        target = self
        if target:
            hero.command(paladin, "cast", "heal", target)
    elif (paladin.health < paladin.maxHealth * 0.3):
        hero.command(paladin, "shield")
    else:
        if enemyattack:
            hero.command(paladin, "attack", enemyattack)


def CommandSoldier(soldier):
    enemy = soldier.findNearestEnemy()
    if enemy:
        hero.command(soldier, "attack", enemy)


def CommandArcher(soldier):
    if enemyattack:
        hero.command(soldier, "attack", enemyattack)


def CommandPeasant(soldier):
    if enemyattack:
        hero.command(soldier, "attack", enemyattack)


def lowestHealthFriend():
    lowestHealth = 99999
    lowestFriend = None
    friends = hero.findFriends()
    for friend in friends:
        if friend.health < lowestHealth and friend.health < friend.maxHealth:
            lowestHealth = friend.health
            lowestFriend = friend

    return lowestFriend


while True:
    summonTroops()
    commandTroops()
    items = hero.findItems()
    if (len(items) > 0 and hero.health < hero.maxHealth * 0.5):
        pickUpNearestItem(items)
    else:
        enemyattack = findTarget()
        if (enemyattack):
            attack(enemyattack)
        else:
            hero.shield()
