// const multiply = (a, b) => {
//     return a*b
// }
// console.log(multiply(44, 28))

let reverse = []
const sortWords = (words) => {
    const sorted = words.split(" ").sort()
    for (const word of sorted) {
        reverse.unshift(word)
    }

    const midOdd = sorted[Math.floor(sorted.length * 0.5)]
    // return sorted[0]
    return midOdd
}

console.log(sortWords("race rabbit red rain ring"))
// console.log(reverse)





// 33 x 43
// 28 x 28
// 27 x 18

const question = "calculate the volume of a sphere with radius 5cm. (Take pi = 22/7)"

const ans = Math.pow(5, 3)*Math.PI*4/3

console.log(ans)
