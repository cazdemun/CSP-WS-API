
const express = require('express');
const WebSocket = require('ws');
const mongoose = require('mongoose')
const Profile = require('./models/profile')
// Add some kind of logger as a dependency
// Add env. variables so it can spit mocked data

// This should be an env. variable
const URI = "mongodb+srv://charles:adminfo2018@cluster0-jwsrk.mongodb.net/test?retryWrites=true&w=majority"

mongoose.connect(URI)
mongoose.connection.once('open', ()=> {
  console.log("Connected to database")
})

// ws://localhost:8081/training/feedback - { "message": "Rock it with HTML5 WebSocket" }
const wss = new WebSocket.Server({ port: 8081, path: "/training/feedback" });

wss.on('connection', connection = (ws) => {
  ws.on('message', incoming = (message) => {
    msg = JSON.parse(message)
    console.log('received: %s', msg.message);
    ws.send('left or right with a %');
  });
  
  ws.send('Openning feedback channel');
});

const app = express();

app.use(express.json());

app.post("/training/start",(req, res) => {
  if (!req.body.userid) {
    res.status(400).send('User not found');
  } else { 
    Profile.findOne({ userid: req.body.userid })
    .then(p => {
      let userid = p.userid,
        state = p.state + 1;
      let args = userid + " " + state
      
      // There are synchronization troubles, i.e. 
      // this timestamp is approx 4 seconds earlier than the python script
      let timestamp = Math.floor(Date.now() / 1000);

      let spawn = require("child_process").spawn; 
      let process = spawn('cmd.exe', ['/c', "conda activate & python ./cortex/cortexsaver.py " + args]);
      
      process.stdout.on('data', data => {
        // Note: This is excuted at least three times
        // Maybe can be solved printing just one time
        console.log(data.toString()); 
        // update
      }); 
      
      process.stderr.on('data', err => {
        console.error(err.toString());
        res.status(500).send("Something went wrong with the python script");
      });
      
      p.state = p.state + 1
      p.timestamps.push(timestamp)
      
      // Acto de fe en que no habran errores en el script de python
      p.save()
      .then(_ => console.log("Updated"))
      .catch(err => console.log(err))

      res.send("Saving for user: " + req.body.userid);
      console.log("Saving for user:", req.body.userid);
    })
    .catch(err => {
      res.status(500).send(err)
      console.log(err)
    })
  }
})

// app.post("/training/mark",(req, res) => {
//   res.send("Mark halfway for annotations")
// })

// app.post("/training/confirm",(req, res) => {
//   res.send("There were no errors recording")
// })

app.get("/user",(_, res) => {
  Profile.find({})
  .then(data => {
    res.send(data)
  })
  .catch(err => {
    console.log(err)
    res.send(err)
  })
})

app.post("/user",(req, res) => {
  if (!req.body.userid) {
    res.status(400).send('User not found');
  } else {
    let profile = new Profile({
      userid: req.body.userid,
      state: 0,
      protocol: 'graz',
      timestamps: []
    })

    profile.save(err => {
      if (err) { 
        res.send(err)
        console.log(err)
      } else {
        res.send("User added")
        console.log("User added")
      }
    })
  }

  // let user = users.filter(u => u.id === req.body.id)
  // res.send(user.shift())
})

app.get("/user/:userid",(req, res) => {
  Profile.findOne({ userid: req.params.userid })
  .then(p => { 
    res.send(p)
  })
  .catch(err => res.status(500).send(err))
})

app.post("/user/:userid",(req, res) => {
  // let user = users.filter(u => u.id === req.body.id)
  // res.send(user.shift())
})


// 128 hz

app.listen(4000, () => {
  console.log("Now listening on the port 4000")
})