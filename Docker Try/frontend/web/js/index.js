new Vue({
    el: '#login',
    data: {
        username: null,
        password: null,
        message: null,
    },
    mounted: function() {
        log = localStorage.getItem('loggedin')
        if (log != null){
            window.location.href = 'home.html'
        }
    },
    methods: {
        signUp() {
            axios.post('http://192.168.99.100:8000/',
            {
                username: this.username,
                password: this.password,
            })
            .then(response => {this.message = response.data})
        },
        signIn() {
            axios.post('http://192.168.99.100:8000/signin', 
            {
                username: this.username,
                password: this.password,
            })
            .then(response => 
                {
                    if (response.data != '0') 
                        {
                            localStorage.setItem('loggedin', response.data)
                            window.location.href = 'home.html'
                        }
                    else {
                        this.message = `Invalid Inputs` ;
                    }
                })
        },
    },
})