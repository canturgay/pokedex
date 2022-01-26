<template>
  <div>
    <b-col sm="7" md="6" class="pagination">
    <b-pagination
      :total-rows="totalRows"
      v-model="currentPage"
      :per-page="perPage"
      align="fill"
      aria-controls="poke_table"
    ></b-pagination>
    </b-col>
    <b-table id="poke_table" :items="poke_list" :fields="fields" :per-page="perPage" :current-page="currentPage" striped hover responsive="sm" ref="table">
      <template #cell(show_details)="row">
        <b-button size="sm" @click="row.toggleDetails" class="mr-2">
          {{ row.detailsShowing ? 'Less' : 'More'}}
        </b-button>
      </template>
      <template #cell(identifier)="data">
        <b-form-input v-if="poke_list[data.index].isEdit" type="text" v-model="poke_list[data.index].identifier" @change="submitField(poke_list[data.index].order, [data.value, 'identifier'])"></b-form-input>
        <span v-else>{{ data.value }}</span>
      </template>
      <template #cell(height)="data">
        <b-form-input v-if="poke_list[data.index].isEdit" type="number" v-model="poke_list[data.index].height" @change="submitField(poke_list[data.index].order, [data.value, 'height'])"></b-form-input>
        <span v-else>{{ data.value }}</span>
      </template>
      <template #cell(weight)="data">
        <b-form-input v-if="poke_list[data.index].isEdit" type="number" v-model="poke_list[data.index].weight" @change="submitField(poke_list[data.index].order, [data.value, 'weight'])"></b-form-input>
        <span v-else>{{ data.value }}</span>
      </template>
      <template #cell(base_experience)="data">
        <b-form-input v-if="poke_list[data.index].isEdit" type="number" v-model="poke_list[data.index].base_experience" @change="submitField(poke_list[data.index].order, [data.value, 'base_experience'])"></b-form-input>
        <span v-else>{{ data.value }}</span>
      </template>

      <template #row-details="row">
        <b-card>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Species:</b></b-col>
            <b-form-input v-if="poke_list[row.index].isEdit" type='number' v-model="poke_list[row.index].species_id" @change="submitField(poke_list[row.index].order, [row.value, 'species_id'])"></b-form-input>
            <b-col v-else>{{ row.item.species_id }}</b-col>
          </b-row>

          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Is Default:</b></b-col>
            <b-form-select v-if="poke_list[row.index].isEdit" v-model="poke_list[row.index].is_default" :options="[true, false]" @change="submitField(poke_list[row.index].order, [poke_list[row.index].is_default, 'is_default'])"></b-form-select>
            <b-col>{{ row.item.is_default }}</b-col>
          </b-row>
        </b-card>
      </template>
      <template #cell(edit)="data">
        <b-button @click="editRowHandler(data)" >
          <span v-if="!poke_list[data.index].isEdit">Edit</span>
          <span v-else>Done</span>
        </b-button>
      </template>
    </b-table>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'Pokedex',
  data () {
    return {
      pokemons: Object,
      poke_list: undefined,
      perPage: 20,
      currentPage: 1,
      totalRows: 10194,
      fields: [
        {key: 'identifier', label: 'Name'},
        {key: 'height', label: 'Height'},
        {key: 'weight', label: 'Weight'},
        {key: 'base_experience', label: 'Experience'},
        {key: 'show_details', label: ''},
        {key: 'edit', label: ''}
      ]
    }
  },

  async created () {
    await this.getPokemons()
  },

  methods: {
    getPokemons () {
      axios.get('http://127.0.0.1:5000/api/pokemons')
        .then(response => {
          this.pokemons = JSON.parse(response.data)
          this.$store.commit('setPokemons', this.pokemons)
          this.poke_list = this.$store.getters.getPokemons
        })
        .catch(error => {
          console.log(error)
        })
    },
    editRowHandler (data) {
      this.poke_list[data.index].isEdit = !this.poke_list[data.index].isEdit
      this.$refs.table.refresh()
    },
    submitField (index, load) {
      axios.put('http://127.0.0.1:5000/api/pokemons/' + index, {load})
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
