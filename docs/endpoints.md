# API v1

Get a real time prediction

    WS /training/feedback 

Save a task

    POST /training/start 

Force to train/load a model

    POST /training/train 

Get daemon state info

    GET /daemon/info 

Get all users

    GET /users 

Create a new user

    POST /users 

Get one user

    GET /users/:userid 

Delete, change to DELETE

    POST users/:userid 

# API v2

## Daemon

Get daemon state info

    GET api/v2/daemon/state

Force to train/load a model

    POST api/v2/daemon/choose-model 

Opens a feedback channel to get real time predictions 

    WS api/v2/daemon/feedback 


## Users

Get all users

    GET api/v2/users 

Create a new user

    POST api/v2/users 

Get one user

    GET api/v2/users/:userid 

(Soft) Delete a user 

    DELETE api/v2/users/:userid 

Get user progress

    GET api/v2/users/:userid/progress 

Get user progress on one protocol

    GET api/v2/users/:userid/progress/:protocolid

## Protocols

Get all protocols

    GET api/v2/protocols

Get one protocol

    GET api/v2/protocol/:protocolid 

## Tasks

Get all tasks trained/saved of a user

    GET api/v2/users/:userid/tasks 

Create/train/save a task

    POST api/v2/users/:userid/tasks 

Get one task trained/saved of a user

    GET api/v2/users/:userid/tasks/:taskid 

Edit one task of a user (especifying a training protocol or mode)

    PUT api/v2/users/:userid/tasks/:taskid 

# Model

Classifier = String | CSP

DaemonState = DaemonCortexState | DaemonSimulatorState

DaemonCortexState = 
{ user : Maybe User
, classifier: Maybe Classifier
, credentials : String
}

DaemonSimulatorState =
{ user : Maybe User
, classifier: Maybe Classifier
}

state :: () -> DaemonState

task :: () -> Task

predict :: String -> Movement

trainModel :: DaemonState -> DaemonState

toJson :: a -> JSON

