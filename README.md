# Robot City Navigation System

A Robot City Navigator System.

#### Features

* create a random route
* save the random route
* create a route from a file
* run a robot within the random route
* run a robot within an available route
* show list of available routes

#### Dependencies

* python3

## Usage


### manage.py

*manage.py* is a main script to interact with a user through Terminal.

Try start with help

```
python manage.py --help
```

To show a list available routes

```
python manage.py --list
```

To create a random route

```
python manage.py --random
```

... to save the randomly created route

```
python manage.py --random --save
```

To run the available route

```
python manage.py --route f033cb84136c4d68b3964b8c6ad7a037.json
```

To create a new route from a file

```
python manage.py --file ./my_file.txt
```

Some of the options have a shortness, check Help.

### Route File

You can feed a regular **.txt** file

##### Example:

```
Start at (110, 450)
Go North 5 blocks
Turn right
Go until you reach landmark "Statue of Old Man with Large Hat"
Go West 25 blocks
Turn left
Go 3 blocks
```

##### Where:

* *start at* - teleport a robot and stands for as a start position
* *turn* - turn robot
* *go (direction|destination)* - instruction to turn (if there is a direction), move forward

### test.py

You can run test:

```
python test.py
```

## About

I made a simple implementation, covered by tests (not full),
which is able to resolve base required tasks.

### Answers

**A system with millions of routes vs. a system with <100 routes**

and

**A system where routes have thousands of instructions each vs. a system where
routes have 1-10 instructions**

In a perfect useful condition the *route* is a Graph.
So, RDBMS will be pretty slow with a big Graph.
The better way is make integration with NoSQL database,
or even better with graph database (for example, Neo4j).

A current way os storing routes is simple, and good to illustrate a work.

**A system with millions of simultaneous users vs. <10 simultaneous users**

The system supposed to be performed as a web service,
there are many ways to scale it on demand,
for example through Docker containers.

A current version does not support a User as a content type.

**A system where routes are frequently changed and updated vs. one where
routes are permanent once initially devised**

If routes will be permanent,
it will acceptable to use RDBMS with FK-s between route points,
and weights.
Otherwise, updates of a Graph will be a pain.

### TODO:

* integrate into a web server
* provide interfaces to create, edit, and delete routes
* landmarks
* move to a scalable graph database (Neo4j, etc.)
