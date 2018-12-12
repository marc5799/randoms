new Vue({
    el: '#edit',
    data: {
        items: [],
        bought_id: null,
        name: null,
        price: null,
        image: null,
        message: null,
    },
    mounted: function() {
        axios({
            method: 'get',
            url: '/api/youritems'
        })
        .then(response => {this.items = response.data})
    },
    methods: {
        editItem() {
            axios.post('/api/edit',
            {
                name: this.name,
                price: this.price,
                image: this.image,
                bought_id: '4',
            })
            .then(response => {
                this.message = response.data
            })
        },
        deleteItem() {
            axios.post('/api/delete',
            {
                bought_id: '4',
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