new Vue({
    el: '#buy',
    data: {
        items: [],
        bought_id: null,
    },
    mounted: function() {
        axios({
            method: 'get',
            url: '/api/items'
        })
        .then(response => {this.items = response.data})
    },
    methods: {
        buyItem: function() {
            localStorage.setItem('bought_id', this.bought_id)
            window.location.href = 'buyitem.html'
        },
        logOut() {
            axios.post('/api/logout',
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