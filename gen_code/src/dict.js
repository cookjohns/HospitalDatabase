var fs = require('fs');

//Creates a dictionary that acts as a singleton for
//dictionaries with the same id. Optionally shuffles words.
var Dictionary = function(id, file_name_path, regex = /\n/, shuffle = true)
{
   //return existing dictionary
   if(id in Dictionary.prototype.ids) {
      return Dictionary.prototype.ids[id];
   }

   var input = fs.readFileSync(file_name_path);
   if (!(regex instanceof RegExp)) {
      console.error('Regular expresion is not a regex');
      console.log(regex);
      return "Error";
   }

   var dict = input.toString().split(regex);

   //local property updates
   this.id = id;
   this.dict = dict;

   //permutate dictionary
   if (shuffle === true) {
      this.shuffle();
   }

   //create singleton
   Dictionary.prototype.ids[this.id] = this;
}

//list of currently active dictionaries
Dictionary.prototype.ids = [];

//outputs random defintion
Dictionary.prototype.rnd_def = function(n) {
   //let user decide size of selection
   //with an invariant that prevents overflows
   return this.dict[Math.floor(Math.random() * this.dict.length) % n];
}

//Shuffles dictionary
//influence from project in alg
Dictionary.prototype.shuffle = function() {
   var swap = function(i1, i2, arr) {
      var temp = arr[i1];
      arr[i1] = arr[i2];
      arr[i2] = temp;
   }
      
   for (var i = 0; i < this.dict.length; i++)
      swap(i, Math.floor(Math.random()*this.dict.length), this.dict);
}


module.exports = {Dictionary: Dictionary};
