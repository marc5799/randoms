new Vue({
    el: '#home',
    data: {
    },
    mounted: function() {
        logged = localStorage.getItem('loggedin')
        if (logged == null){
            window.location.href = 'login.html'
        }
    },
    methods: {
        logOut() {
            axios.post('http://192.168.99.100:8000/logout',
            {
                logged: "0",
            })
            .then(response => {
                localStorage.clear();
                window.location.href = 'login.html'
            })
        },
    },
})