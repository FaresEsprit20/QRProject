const mongoose = require("mongoose");

const certificateSchema = mongoose.Schema(
    {
        image: String
    }
);

const Certificate = mongoose.model("certificate", certificateSchema);

module.exports = Certificate;