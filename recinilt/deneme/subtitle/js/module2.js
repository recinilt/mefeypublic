var mymodule = (function(){
    //IIFE
    //private members:
    let number = 0;
    
    let increment = function(){
        return ++number;
    };

    let decrement = function(){
        return --number;
    };

    let toplama = function (num1,num2) {
        return num1 + num2;
    }

    //public members:
    return {
        increment,
        decrement,
        toplama,
        publicMethod1 : function(){console.log("publicmethod1")},
        publicMethod2 : function(){console.log("publicmethod2")}
    }
})();

console.log(mymodule.increment());
console.log(mymodule.increment());
console.log(mymodule.increment());
console.log(mymodule.decrement());
console.log(mymodule.publicMethod1());
console.log(mymodule.toplama(2,3));

document.getElementById("sonuc").innerHTML=mymodule.toplama(85,94);
