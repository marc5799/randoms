new Vue({
    el: '#buyitem',
    data: {
        bought_item: [],
        item: [],
        id_item: null,
        cc: null,
    },
    mounted: function() {
        axios.post('http://192.168.99.100:8000/boughtitem',
        {
            id_item: localStorage.getItem('bought_id')
        })
        .then(response => {this.bought_item = response.data})
    },
    methods: {
        buy() {
            axios.post('http://192.168.99.100:8000/buy', 
            {
                cc: this.cc,
                bought_id: localStorage.getItem('bought_id'),
            })
            .then(response => {
                window.location.href = 'home.html'
            })
        },
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