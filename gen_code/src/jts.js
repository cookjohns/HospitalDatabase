var jsontosql = function(data, data_model)
{
   var sql = [];
   data.elem.forEach((tuple) => {
      var temp1 = 0;
      var temp2 = 0;
      sql.push("insert into " + data.name +
               "(" +
               tuple.reduce((prev, attr) => {
                  temp1 += attr.name.length + 1;
                  return prev + attr.name + ',';
               }, "").substring(0, temp1 - 1) + ")" +
               " values" + "(" + 
               tuple.reduce((prev, attr) => {
                  //makes sure value is always of string type
                  temp2 += attr.value.toString().length + 3;
                  return prev + '"' + attr.value + '",';
               }, "").substring(0, temp2 - 1) + ");"); 
   });

   return sql;
}

module.exports = {jsontosql};
