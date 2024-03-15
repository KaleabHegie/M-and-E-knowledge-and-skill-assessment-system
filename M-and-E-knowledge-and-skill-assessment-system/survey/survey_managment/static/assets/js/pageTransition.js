
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('show')
        }
        else {
            entry.target.classList.remove('show')
        }
    })
})

const hiddenElememts = document.querySelectorAll('.hidden-transition')

//  what the above observer should observe
hiddenElememts.forEach((el) => observer.observe(el))