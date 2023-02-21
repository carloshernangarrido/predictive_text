
// Data types:

// ******* Primitives / Value Types *******
// *** Variables ***
let firstName = 'Hernán'; // string
let age = 39; // number
let flag = true; // boolean
let aNullVariable = null; // null
let anUndefinedVariable // undefined
// *** Constants ***
const pi = 3.1415

// ******* Reference Types *******
// *** object ***
let person = {
    firstName: "Hernán",
    lastName: "Garrido",
    age: 39
}
// dot notation
person.age = person.age + 1
// bracket notation
person['firstName'] = 'Carlos'

// *** array ***
myArray = ['1', 1, person]

// *** function ***
function suma(a, b) {
    console.log('Function suma running...')
    return(((a**2+b**2)**(1/2))/(2**(1/2)))
}

// ******* logging *******
// pi = 3.1 TypeError
console.log(firstName, pi);
console.log(person);
console.log(person.age);
console.log("the full array is:", myArray, "\nthe first element is: ", myArray[0])
console.log("The root mean square of 2 and 3 is:", 
            suma(2, 3));