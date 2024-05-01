const a = ["Apple", "Boy", "Cat", "Dog"];
const b = ["Dog", "Cat"]; // Example array of search terms

const arraySet = new Set(array);
const x = searchTerm.some(term => arraySet.has(term));

console.log(x);