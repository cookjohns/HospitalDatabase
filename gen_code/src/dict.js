var fs = require('fs');

var Dictionary = function(id, regex, file_name_path, shuffle)
{
   if(id in Dictionary.prototype.ids) {
      return Dictionary.prototype.ids[id];
   }

   var input = fs.readFileSync(file_name_path);
   //if (!(regex instanceof RegExp)) {
   //   console.error('Regular expresion is not a regex');
   //   console.log(regex);
   //   return "Error";
   //}

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

Dictionary.prototype.ids = [];

Dictionary.prototype.rnd_def = function(n) {
   //let user decide size of selection
   //with an invariant that prevents overflows
   return this.dict[Math.random(0, n) % this.dict.length];
}

//influence from project in alg
Dictionary.prototype.shuffle = function() {
   var swap = function(e1, e2) {
      var temp = e1;
      e1 = e2;
      e2 = temp;
   }
      
   for (var i = 0; i < this.dict.length; i++)
      swap(this.dict[i], this.dict[Math.random(0, this.dict.length)]);
}


module.exports = {Dictionary: Dictionary};
