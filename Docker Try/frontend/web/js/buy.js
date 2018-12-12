new Vue({
    el: '#buy',
    data: {
        items: [],
        bought_id: null,
    },
    mounted: function() {
        axios({
            method: 'get',
            url: 'http://localhost:5000/items'
        })
        .then(response => {this.items = response.data})
    },
    methods: {
        buyItem: function() {
            localStorage.setItem('bought_id', '1')
            window.location.href = 'buyitem.html'
        },
        logOut() {
            axios.post('http://localhost:5000/logout',
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