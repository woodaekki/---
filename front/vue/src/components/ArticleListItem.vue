<!-- ArticleListIte.vue -->

<template>
  <RouterLink
    :to="{ name: 'detail', params: { id: article.id } }"
    class="article-item"
  >
    <div class="meta">
      <span class="title">{{ article.title }}</span>
      <span class="preview">{{ article.content }}</span>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>

<style scoped>
.article-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #c5c7ca9d;
  text-decoration: none;
  color: inherit;
  transition: background-color 0.15s ease;
}

.article-item:hover {
  background-color: #f9fafb;
}

.meta {
  display: flex;
  flex-direction: column;
}

.title {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
  color: #111827;
}

.preview {
  font-size: 14px;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 600px;
}


</style>
