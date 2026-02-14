import request from '../utils/axios'

// 用户登录
export const login = (username, password) => {
  return request({
    url: '/user/login',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  })
}

// 用户注册
export const register = (data) => {
  return request({
    url: '/user/register',
    method: 'post',
    data
  })
}

// 获取用户信息
export const getUserInfo = () => {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

// 修改用户信息
export const updateUserInfo = (data) => {
  return request({
    url: '/user/info',
    method: 'put',
    data
  })
}

// 用户登出
export const logout = () => {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

// 角色相关API

// 创建角色
export const createCharacter = (data) => {
  return request({
    url: '/character',
    method: 'post',
    data
  })
}

// 获取用户的所有角色
export const getCharacters = () => {
  return request({
    url: '/character',
    method: 'get'
  })
}

// 获取单个角色信息
export const getCharacter = (characterId) => {
  return request({
    url: `/character/${characterId}`,
    method: 'get'
  })
}

// 更新角色信息
export const updateCharacter = (characterId, data) => {
  return request({
    url: `/character/${characterId}`,
    method: 'put',
    data
  })
}

// 删除角色
export const deleteCharacter = (characterId) => {
  return request({
    url: `/character/${characterId}`,
    method: 'delete'
  })
}

// 获取角色数量
export const getCharacterCount = () => {
  return request({
    url: '/character/count',
    method: 'get'
  })
}

// 等级相关API

// 获取角色等级信息
export const getCharacterLevel = (characterId) => {
  return request({
    url: `/level/${characterId}`,
    method: 'get'
  })
}

// 角色获取经验值
export const gainExp = (characterId, exp) => {
  return request({
    url: '/level/gain-exp',
    method: 'post',
    data: {
      character_id: characterId,
      exp: exp
    }
  })
}

// 获取所有角色等级信息
export const getCharactersLevel = () => {
  return request({
    url: '/level',
    method: 'get'
  })
}

// 装备相关API

// 创建装备
export const createEquipment = (data) => {
  return request({
    url: '/equipment',
    method: 'post',
    data
  })
}

// 获取装备列表
export const getEquipmentList = () => {
  return request({
    url: '/equipment',
    method: 'get'
  })
}

// 获取单个装备信息
export const getEquipment = (equipmentId) => {
  return request({
    url: `/equipment/${equipmentId}`,
    method: 'get'
  })
}

// 穿戴装备
export const equipEquipment = (data) => {
  return request({
    url: '/equipment/equip',
    method: 'post',
    data
  })
}

// 卸下装备
export const unequipEquipment = (slotId) => {
  return request({
    url: `/equipment/unequip/${slotId}`,
    method: 'delete'
  })
}

// 获取角色已穿戴的装备
export const getCharacterEquipment = (characterId) => {
  return request({
    url: `/equipment/character/${characterId}`,
    method: 'get'
  })
}

// 排行榜相关API

// 获取等级排行榜
export const getLevelRanking = () => {
  return request({
    url: '/ranking/level',
    method: 'get'
  })
}

// 获取战力排行榜
export const getPowerRanking = () => {
  return request({
    url: '/ranking/power',
    method: 'get'
  })
}