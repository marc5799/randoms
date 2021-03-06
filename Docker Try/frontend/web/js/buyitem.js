new Vue({
    el: '#buyitem',
    data: {
        bought_item: null,
        item: [],
        id_item: null,
        cc: null,
        message: null,
    },
    mounted: function() {
        axios.post('/api/boughtitem',
        {
            id_item: localStorage.getItem('bought_id')
        })
        .then(response => {this.bought_item = response.data})
    },
    methods: {
        buy() {
            axios.post('/api/buy', 
            {
                cc: this.cc,
                bought_id: localStorage.getItem('bought_id'),
            })
            .then(response => {
                this.message = response.data
            })
        },
        logOut() {
            axios.post('/api/logout',
            {
                logged: "0",
            })
            .then(response => {
                localStorage.clear();
                window.location.href = '/login.html'
            })
        },
    },
})