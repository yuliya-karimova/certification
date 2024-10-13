<template>
  <div class="file-upload">
    <input
      type="file"
      accept=".docx,.pdf"
      @change="onFileChange"
      class="bg-primary-700 hover:bg-primary-600 transition p-2 rounded-xl text-white cursor-pointer"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCheckStore } from '@/stores/check'

const selectedFile = ref<File | null>(null)
const checkStore = useCheckStore()

const emit = defineEmits(['uploaded'])

const onFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files ? target.files[0] : null
  if (file) {
    selectedFile.value = file

    await uploadSelectedFile()
  }
}

const uploadSelectedFile = async () => {
  if (selectedFile.value) {
    const result = await checkStore.uploadFile(selectedFile.value)
    emit('uploaded', result, selectedFile.value.name)
  }
}
</script>

<style scoped>
.file-upload {
  display: flex;
  gap: 1rem;
  align-items: center;
}
</style>
