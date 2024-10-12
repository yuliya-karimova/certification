import { defineStore } from 'pinia'
import axios from 'axios'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

interface CheckResultInterface {
  // docx: string
  // pdf: string
  text: string
}

interface CheckState {
  checkResult: CheckResultInterface | null
}

export const useCheckStore = defineStore('check', {
  state: (): CheckState => ({
    checkResult: null,
  }),
  actions: {
    async checkUseCase(text: string): Promise<string> {
      try {
        const response = await axios.post(`${apiBaseUrl}/api/check-use-case`, { text })
        return response.data.data
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось проверить требования'
      }
    },
    async checkObjects(text: string): Promise<string> {
      try {
        const response = await axios.post(`${apiBaseUrl}/api/check-regulation-objects`, { text })
        return response.data.data
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось проверить требования'
      }
    },
    async checkRegulations(text: string): Promise<string> {
      try {
        const response = await axios.post(`${apiBaseUrl}/api/check-regulations`, { text })
        return response.data.data
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось проверить требования'
      }
    },
    // async check(dialog: DialogItem[]): Promise<string> {
    //   try {
    //     const response = await axios.post(`${apiBaseUrl}/api/check`, { texts: dialog })
    //     return response.data.data
    //   } catch (err: any) {
    //     return err.response?.data?.error || 'Не удалось проверить требования'
    //   }
    // },
    // async correct(dialog: DialogItem[]): Promise<string> {
    //   try {
    //     const response = await axios.post(`${apiBaseUrl}/api/correct`, { texts: dialog })
    //     return response.data.data
    //   } catch (err: any) {
    //     return err.response?.data?.error || 'Не удалось уточнить требования'
    //   }
    // },
  }
})
