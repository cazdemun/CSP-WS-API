const mongoose = require('mongoose')
const Schema = mongoose.Schema;

const userid = { type: String, index: { unique: true }}

const profileSchema = new Schema({
  userid: userid,
  state: Number,
  protocol: String,
  timestamps: [Number]
})

module.exports = mongoose.model('Profile', profileSchema)