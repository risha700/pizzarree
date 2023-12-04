
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue'), name:'Home' },
      { path: '/checkout', component: () => import('pages/shop/CheckoutPage.vue'), name:'Checkout' },

    ]
  },
  {
    path: '/shop',
    component: () => import('layouts/ShopLayout.vue'),
    children: [
      { path: 'menu', component: () => import('pages/shop/MenuPage.vue'), name:'Menu' },
      { path: 'checkout', component: () => import('pages/shop/CheckoutPage.vue'), name:'Checkout' },
      { path: 'cart', component: () => import('pages/shop/CartPage.vue'), name:'Cart' },
    ]
  },
  {
    path: '/user',
    name:'User',
    component: () => import(/* webpackChunkName: "group-user" */ "layouts/UserLayout.vue"),
    children: [
      { path: 'login', component: () => import('pages/user/LoginPage.vue'), name:'Login', meta: {requiresAuth: false} },
      { path: 'register', component: () => import('pages/user/RegisterPage.vue'), name:'Register', meta: {requiresAuth: false}  },
      { path: 'password_reset', component: () => import('pages/user/PasswordReset.vue'), name:'PasswordReset', meta: {requiresAuth: false}  },
      { path: 'password_reset_confirm', component: () => import('pages/user/PasswordResetConfirm.vue'), name:'PasswordResetConfirm', meta: {requiresAuth: false} },
      { path: 'password_change', component: () => import('pages/user/PasswordChange.vue'), name:'PasswordChange', meta: {requiresAuth: true} },
      { path: 'dashboard', component: () => import('pages/user/DashboardPage.vue'), name:'Dashboard', meta: {requiresAuth: true} },


    ]
  },
  {
    path: "/done",
    name: "Done",
    component: () => import("pages/user/WebhookDone.vue"),
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
