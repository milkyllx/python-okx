<template>
    <header class="header">
        <div class="container nav-container">
            <div class="logo">币投网</div>
            <nav class="nav-links">
                <a href="#" class="active">首页</a>
                <a href="#">功能</a>
                <a href="#">解决方案</a>
                <a href="#">价格</a>
                <a href="#">学习</a>
                <a href="#">支持</a>
            </nav>
            <div class="nav-buttons">
                <a href="#" class="btn btn-outline">登录</a>
                <a href="#" class="btn btn-primary">立即注册</a>
            </div>
        </div>
    </header>
</template>

<script>
export default {
    name: 'HeaderComponent'
}
</script>

<style scoped>
.header {
    background-color: var(--bg-light);
    padding: 16px 0;
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.logo {
    font-size: 24px;
    font-weight: 700;
}
.nav-links a {
    color: var(--text-primary);
    text-decoration: none;
    margin: 0 16px;
    font-size: 16px;
    transition: color 0.3s;
}
.nav-links a:hover, .nav-links a.active {
    color: var(--accent-color);
}
.nav-buttons .btn {
    margin-left: 16px;
}
</style>