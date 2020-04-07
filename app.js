const express = require('express');
const WebSocket = require('ws');
const dotenv = require('dotenv');
const cors = require('cors');
const mongoose = require('mongoose')
const Profile = require('./models/profile')

dotenv.config();

// Add some kind of logger as a dependency

// .env file bug on prod
PORT=4000
WS_PORT=8081
ATLAS_URI="mongodb+srv://charles:adminfo2018@cluster0-jwsrk.mongodb.net/test?retryWrites=true&w=majority"

mongoose.connect(ATLAS_URI, {
  useCreateIndex: true,
  useUnifiedTopology: true,
  useNewUrlParser: true
})

mongoose.connection.once('open', () => {
  console.log("Connected to database")
})

////////////////////////////////////////////////////////////////////////////////////////////////////////////

const daemon = new WebSocket('ws://localhost:8765/');

daemon.on('open', () => {
  console.log("Connected to daemon")
})

daemon.on('message', (data, flags) => {
  console.log('\x1b[33m%s\x1b[0m', data);
});

daemon.on('error', (data, flags) => {
  console.log("from global an error")
  console.log(data)
});

const errorHandler = (res, err, status = 500) => {
  res.status(status).send(err.message)
  console.log(err)
}

// ws://localhost:8081/training/feedback
const wss = new WebSocket.Server({ port: 8081, path: "/training/feedback" });

wss.on('connection', connection = (client) => {
  client.send("{ \"message\": \"Opening feedback channel\", \"movement\": [0]}");

  // There are some issues with multiple clients
  let handlePrediction = (event) => {
    data = JSON.parse(event.data)
    if (data.movement) {
      console.log("from wss:")
      console.log(data)
      client.send(JSON.stringify(data));
    }
  }

  daemon.addEventListener('message', handlePrediction);

  client.on('message', incoming = (message) => {
    // { "action": "predict", "userid": "charls"}
    console.log('\x1b[36m%s\x1b[0m', `WS /training/feedback`);
    predictMessage = JSON.parse(message)
    console.log('received from client:', predictMessage);
    daemon.send(JSON.stringify(predictMessage));
  });

  client.on('close', () => {
    console.log("Client finished feedback - closing")
    daemon.removeEventListener("message", handlePrediction)
  })
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////
var whitelist = ['http://localhost:3000', '*']
var corsOptions = {
  origin: function (origin, callback) {
    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  }
}


const app = express();
app.use(cors());
app.use(express.json());
app.use((req, res, next) => {
  console.log('\x1b[36m%s\x1b[0m', `${req.method} ${req.originalUrl}`);
  next();
});

// Training related

// rename to training/record or training/save
app.post("/training/start", (req, res) => {
  if (!req.body.userid)
    return res.status(400).send('User not found');

  Profile
    .findOne({ userid: req.body.userid })
    .then(profile => {
      if (profile === null)
        throw new Error("User not found!")

      let userid = profile.userid, state = profile.state + 1;
      let timestamp = Math.floor(Date.now() / 1000);

      // Save
      saveMessage = {
        action: "save",
        userid: userid,
        state: state,
        timestamp: timestamp
      }
      daemon.send(JSON.stringify(saveMessage));

      // Update
      profile.state = state;
      profile.timestamps.push(timestamp)

      // Acto de fe en que no habran errores en el script de python
      profile.save()
        .then(_ => console.log(`Profile ${userid} updated`))
        .catch(err => console.log(err))

      res.send(JSON.parse(`{ "message": "Saving for user ${req.body.userid}" }`));
      console.log(`Saving for user ${req.body.userid}`);
    })
    .catch(err => {
      res.status(500).send(err.message)
      console.log(`Error: ${err.message}`)
    })

})

app.post("/training/train", (req, res) => {
  if (!req.body.userid) {
    res.status(400).send('User not found');
  } else {
    let userid = req.body.userid;

    trainMessage = {
      action: "train",
      userid: userid
    }

    let handleInfo = (event) => {
      info = JSON.parse(event.data)
      if (info.session_for_training !== undefined) {
        res.send(info);
        daemon.removeEventListener("message", handleInfo)
      }
    }

    daemon.addEventListener('message', handleInfo);
    daemon.send(JSON.stringify(trainMessage));

    console.log(`Training user ${req.body.userid}`);
  }
})

// Daemon Info

// alternative name daemon/status
// res.send("Here we monitor the status of the daemon (credentials, models used and trained, etc)")
app.get("/daemon/info", (_, res) => {
  infoMessage = {
    action: "info"
  }

  let handleInfo = (event) => {
    info = JSON.parse(event.data)
    if (info.session_for_training !== undefined) {
      res.send(info);
      daemon.removeEventListener("message", handleInfo)
    }
  }

  daemon.addEventListener('message', handleInfo);
  daemon.send(JSON.stringify(infoMessage));
})

// Users / Profiles

app.get("/users", (_, res) => {
  Profile.find({})
    .then(data => res.send(data))
    .catch(err => res.send(err))
})

app.post("/users", (req, res) => {
  if (!req.body.userid)
    return res.status(400).send('You need a userid!');

  let profile = new Profile({
    userid: req.body.userid,
    state: 0,
    protocol: 'graz',
    timestamps: []
  })

  profile.save(err => {
    if (err) {
      res.status(500).send(err.errmsg);
      console.log(err.errmsg);
    } else {
      res.send(`User ${req.body.userid} added`);
      console.log(`User ${req.body.userid} added`);
    }
  })
})

app.get("/users/:userid", (req, res) => {
  Profile.findOne({ userid: req.params.userid })
    .then(p => res.send(p))
    .catch(err => res.status(500).send(err))
})

app.post("/users/:userid", (req, res) => {
  // delete user or delete last timestamp
})

app.listen(PORT, () => {
  console.log(`Now listening on the port ${PORT}`)
})