var G_Node = function() {
   this.edges = [];
};

G_Node.prototype.depends_on = function (node)
{
   node.link(this);
};

G_Node.prototype.link = function (node)
{
   if (node in this.edges) {} //do nothing already in there
   //we assume a simple graph
   else {
      this.edges.push(node);
   }
};


//topological sort and dfs modified from Dr. Narayanan Algorithm slides
var topo_sort = function(nodes) {
   var dfs = function(final_callback) {
      var dfs_visit = function(node) {
         node.color = 'gray';
         node.edges.forEach(
         (elem) => {
            if (elem.color == 'white') {
               dfs_visit(elem);
            }
         });
         node.color = 'black';
         
         //insert into sort 
         final_callback(node);
      }
      
      //init nodes for dfs 
      nodes.forEach((node) => {node.color = 'white';});
      //dfs
      nodes.forEach((node) => {if (node.color == 'white') dfs_visit(node)}); 
      //clean up
      nodes.forEach((node) => {delete node.color;});
   }
   
   //call dfs with final call back to topological sort
   var sort = [];
   dfs((elem) => {sort.unshift(elem)});
   return sort;
}
module.exports = {G_Node: G_Node, topo_sort: topo_sort};
