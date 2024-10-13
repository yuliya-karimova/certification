import { defineStore } from 'pinia'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
const userId = uuidv4() // Генерируем уникальный идентификатор (для тестовых целей нет смысла в авторизации)

interface CheckResultInterface {
  docx_url: string
  pdf_url: string
  full_text: string
  excel_url?: string
}

export const useCheckStore = defineStore('check', {
  actions: {
    async checkUseCase(text: string, fileName: string): Promise<CheckResultInterface> {
      try {
        const response = await axios.post(`${apiBaseUrl}/api/check-use-case`, { text, user_id: userId, file_name: fileName })
        return response.data
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось проверить требования'
      }
    },
    async checkObjects(text: string, fileName: string): Promise<CheckResultInterface> {
      try {
        const response = await axios.post(`${apiBaseUrl}/api/check-regulation-objects`, { text, user_id: userId, file_name: fileName })
        return response.data
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось проверить требования'
      }
    },
    async checkRegulations(text: string, fileName: string): Promise<CheckResultInterface> {
      try {
        const response = await axios.post(`${apiBaseUrl}/api/check-regulations`, { text, user_id: userId, file_name: fileName })
        return response.data
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось проверить требования'
      }
    },
    async uploadFile(file: File): Promise<string> {
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await axios.post(`${apiBaseUrl}/api/upload-file`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data.text // Возвращаем текст, извлеченный из файла
      } catch (err: any) {
        return err.response?.data?.error || 'Не удалось загрузить файл'
      }
    },
    getDownloadLink(url: string) {
      return `${apiBaseUrl}${url}`
      // return url
    },
    getUuid() {
      return uuidv4()
    }
  }
})
