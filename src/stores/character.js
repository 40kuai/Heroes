import { defineStore } from 'pinia'

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characters: [],
    currentCharacter: null,
    loading: false,
    error: null
  }),
  getters: {
    getCurrentCharacter: (state) => state.currentCharacter,
    getCharacters: (state) => state.characters
  },
  actions: {
    setCharacters(characters) {
      this.characters = characters
    },
    setCurrentCharacter(character) {
      this.currentCharacter = character
    },
    setLoading(loading) {
      this.loading = loading
    },
    setError(error) {
      this.error = error
    },
    addCharacter(character) {
      this.characters.push(character)
    },
    updateCharacter(characterId, updates) {
      const index = this.characters.findIndex(c => c.id === characterId)
      if (index !== -1) {
        this.characters[index] = { ...this.characters[index], ...updates }
        // 如果更新的是当前角色，也更新currentCharacter
        if (this.currentCharacter && this.currentCharacter.id === characterId) {
          this.currentCharacter = { ...this.currentCharacter, ...updates }
        }
      }
    },
    deleteCharacter(characterId) {
      this.characters = this.characters.filter(c => c.id !== characterId)
      // 如果删除的是当前角色，清空currentCharacter
      if (this.currentCharacter && this.currentCharacter.id === characterId) {
        this.currentCharacter = null
      }
    }
  }
})