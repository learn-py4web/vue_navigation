// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        animals: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.goto_animal = function (a_idx) {
        let a = app.vue.animals[a_idx];
        let a_url = show_animal_base_url + "/" + a.id;
        let button = document.createElement('a');
        button.href = a_url;
        button.click();
    }

    // This contains all the methods.
    app.methods = {
        goto_animal: app.goto_animal,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(get_animals_url).then(function (r) {
            app.vue.animals = app.enumerate(r.data.animals);
        })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
