//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: ':) 欢迎你',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    tf_data: '',
    imgArr: [''],
    username: '',
    toast:'无法连接服务器，请检查网络或联系管理员',
    draw_msg:''
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  shouquan: function(e){
    wx.requestSubscribeMessage({
      tmplIds: ['你的_订阅消息ID'],
      success(res) { }
    })
  },
  submit_album: function () {
    let tf_data;
    this.setData({
      tf_data: this.data.tf_data
    });
    var that=this;
    wx.showLoading({         //后面收到服务器反馈后关闭
      title: '正在绘制...'
    });
    wx.request({
      url: '你的_绘制函数的网络接口', //接口地址
      data: {
        tf_data: this.data.tf_data,
        openid: app.globalData.openid
      },
      header: {
        'content-type': 'application/json' //默认值
      },
      success: function (res) {
        console.log(res.data);
        that.setData({
          imgArr: res.data[0],
          draw_msg: res.data[1]
        });
        wx.hideLoading()    //绘制已经成功
      }
    })
  },
  get_value: function (e) {
    this.setData({
      tf_data: e.detail.value
    })
    console.log('tf_data value got:', e.detail.value)
  },
  previewImage: function (e) {
    var current = e.target.dataset.src;
    wx.previewImage({
      current: current, // 当前显示图片的http链接
      urls: this.data.imgArr // 需要预览的图片http链接列表
    })
  },
  reach_lower: function () {
    console.log('reached!!!')
  },







  onLoad: function () {
    var that = this;
    wx.login({      // 获取当前用户openid
      success: function (res) {
        console.log(res.code)
        //发送请求
        wx.request({
          url: '你的_获取openid的服务器接口', //接口地址
          data: { code: res.code },
          header: {
            'content-type': 'application/json' //默认值
          },
          success: function (res) {
            console.log(res.data);      // open_id
            app.globalData.openid = res.data[0];
            that.setData({
              toast: res.data[1]
            });
            console.log(app.globalData.openid)
          }
        })
      }
    });
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true,
        username: app.globalData.userInfo.nickName
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
  
})
