# Lugo4Py - A Lugo Bots Client

Lugo4Py is a Python implementation of a client player for [Lugo](https://lugobots.dev/) game. 

It **is not a bot** that plays the game, it is only the client to connect to the game server. 

This package implements many methods that does not affect the player intelligence/behaviour/decisions. It is meant to
reduce the developer concerns on communication, protocols, attributes, etc.

Using this client, you just need to implement the Artificial Intelligence of your player and some other few methods to support
your strategy (see the project [exampe](./example/simple) folder).

# Table of Contents
* [Requirements](#requirements)
* [Installation](#Installation)
* [Usage](#usage)
* [First option: Implementing a Bot class (simpler and recommended)](#first-option-implementing-a-bot-class-simpler-and-recommended)
* [Second option: Using reinforcement learning :brain:](#second-option-using-reinforcement-learning-brain)
- [Helpers](#helpers)
  * [Snapshot reader](#snapshot-reader)
  * [Mapper and Region classes](#mapper-and-region-classes)
    + [The Mapper](#the-mapper)
    + [The Region](#the-region)

### requirements 
    
    pip~=23.1.2

### Installation

    pip install lugo4py

### Usage

**Lugo4Py** implements a very basic logic to reduce the code boilerplate. This client will wrap most repetitive
code that handles the raw data got by the bot and will identify the player state.

Implement the [Bot interface](./src/lugo4py/src/interface.py) to handle each player state based on the ball possession.

```python

class Bot(ABC):
    @abstractmethod
    def on_disputing (self, orderSet: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        # on_disputing is called when no one has the ball possession
        pass

    @abstractmethod
    def on_defending (self, orderSet: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        # OnDefending is called when an opponent player has the ball possession
        pass

    @abstractmethod
    def on_holding (self, orderSet: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        # OnHolding is called when this bot has the ball possession
        pass

    @abstractmethod
    def on_supporting (self, orderSet: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        # OnSupporting is called when a teammate player has the ball possession
        pass

    @abstractmethod
    def as_goalkeeper (self, orderSet: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot, state: PLAYER_STATE) -> lugo4py.OrderSet:
        # AsGoalkeeper is only called when this bot is the goalkeeper (number 1). This method is called on every turn,
        # and the player state is passed at the last parameter.
        pass

    @abstractmethod
    def getting_ready (self, snapshot: lugo4py.GameSnapshot):
        # getting_ready will be called before the game starts and after a goal event. You will only need to implement
        # this method in very rare cases.
        pass
```

### First option: Implementing a Bot class (simpler and recommended)

See [example](./example/simple/main.py)

**Lugo4py** client implements the method `play_as_bot(bot)` that expects an instance [bot](src/lugo4py/src/interface.py#L15) implementation.

All you need to do is creating your bot by extending that class and implementing your bot behaviour. See an example
at [example/simple/my_bot.py](example/simple/my_bot.py)


### Second option: Using reinforcement learning :brain:

If you are a **machine learning** enthusiastic you may want to use the Lugo reinforcement learning environment.

**Lugo bots** is an asynchronous game, so you will need to use the **Lugo4py Gym** library to create your model:

See example and documentation at [RL lib readme file](src/lugo4py/rl/src/README.md)


## Kick-start

**Ee encourage you to clone 
[The Dummies Py](https://github.com/lugobots/the-dummies-py)** project and start from there. The read me file will have all
details you need.

### Deploying you bots

After developing your bot, you may share it with other developers.

Please find the instructions for uploading your bot on [lugobots.dev](https://lugobots.dev).

There is a Dockerfile template in [the example directory](./examples) to guide you how to create a container.



## Helpers

There are a many things that you will repeatedly need to do on your bot code, e.g. getting your bot position,
creating a move/kick/catch order, finding your teammates positions, etc.

This package brings a collection of functions that will help you get that data from the game snapshot:


```python

config = lugo4py.EnvVarLoader()

reader = lugo4py.GameSnapshotReader(snapshot, bot.side)
```

### Mapper and Region

This package also provides a quite useful pair: the Mapper and Region classes.

#### The Mapper

`Mapper` slices the field in columns and rows, so your bot does not have to care about precise coordinates or the team
side. The mapper will automatically translate the map position to the bot side.

And you may define how many columns/rows your field will be divided into.

```python

# let's create a map 10x5 
map = lugo4py.Mapper(10, 5, config.get_bot_team_side())

targetRegion = map.get_region(5, 2)

my_region = mapper.get_region_from_point(me.position) 
```

#### The Region

The `Mapper` will slice the field into `Region`s. The Region struct helps your bot to move over the field without caring
about coordinates or team side.

```python
target_region = map.get_region_from_point(bot.position)

region_in_front_of_me = target_region.front()
region_in_back_of_me = target_region.back()
region_in_left_of_me = target_region.left()
region_in_right_of_me = target_region.right()

my_col = target_region.get_col()
my_row = target_region.get_row()

moveOrder, err_ := reader.makeOrderMoveMaxSpeed(position, region_in_front_of_me.center)
```

### Snapshot reader

The Snapshot reader is quite useful. Firs to it helps you to extract data from
the [Game Snapshot](https://github.com/lugobots/protos/blob/master/doc/docs.md#lugo-GameSnapshot) each game turn.

```Python
reader = lugo4py.GameSnapshotReader(snapshot, self.side)
reader.get_my_team()
reader.get_team(side)
reader.is_ball_holder(player)
reader.get_opponent_side()
reader.get_my_goal()
reader.get_opponent_goal()
reader.get_player(side, number)
```
And also help us to create
the [Turn Orders Set](https://github.com/lugobots/protos/blob/master/doc/docs.md#lugo-OrderSet) based on the game state
and our bot team side:

```Python
reader = lugo4py.GameSnapshotReader(snapshot, bot.side)
reader.make_order_jump(origin, target, speed)
reader.make_order_kick(ball, target, speed)
reader.make_order_kick_max_speed(ball, target)
reader.make_order_move(origin, target, speed)
reader.make_order_move_from_vector(direction, speed)
reader.make_order_move_max_speed(origin, target)
reader.make_order_catch()
```

And, last but not least, the Reader also helps our bot to see the game map based on directions instead of coordinates:

```Python
reader.make_order_move_by_direction(DIRECTION.FORWARD)
reader.make_order_move_by_direction(DIRECTION.BACKWARD)
reader.make_order_move_by_direction(DIRECTION.LEFT)
reader.make_order_move_by_direction(DIRECTION.RIGHT)
reader.make_order_move_by_direction(DIRECTION.BACKWARD_LEFT)
reader.make_order_move_by_direction(DIRECTION.BACKWARD_RIGHT)
reader.make_order_move_by_direction(DIRECTION.FORWARD_LEFT)
reader.make_order_move_by_direction(DIRECTION.FORWARD_RIGHT)
```
## The trainable bot

The trainable bot is an interface defined [here](src/lugo4py/rl/src/interfaces.py)


```
docker run -p 8080:8080 -p 5000:5000 lugobots/server:latest play --dev-mode --timer-mode=remote

python3 -m example.rl.main
```
