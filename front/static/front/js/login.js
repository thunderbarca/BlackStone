$(document).ready(function(){
	//登陆表单验证
	$("#loginForm").validate({
		rules:{
			username:{
				required:true,//必填
				minlength:2, //最少2个字符
				maxlength:10,//最多10个字符
			},
			password:{
				required:true,
				minlength:2,
				maxlength:10,
			},
		},
		//错误信息提示
		messages:{
			username:{
				required:"必须填写用户名",
				minlength:"用户名至少为6个字符",
				maxlength:"用户名至多为20个字符",
				remote: "用户名已存在",
			},
			password:{
				required:"必须填写密码",
				minlength:"密码至少为6个字符",
				maxlength:"密码至多为20个字符",
			},
			validateCode:{
				required:"请输入验证码",
				validateCode: "请输入正确的验证码"
			}
		},

	});
	//注册表单验证
	$("#registerForm").validate({
		rules:{
			username:{
				required:true,//必填
				minlength:2, //最少2个字符
				maxlength:10,//最多10个字符
				remote:{
					url:"http://kouss.com/demo/Sharelink/remote.json",//用户名重复检查，别跨域调用
					type:"post",
				},
			},
			password:{
				required:true,
				minlength:6, 
				maxlength:20,
			},
			email:{
				required:true,
				email:true,
			},
			confirm_password:{
				required:true,
				minlength:6,
				equalTo:'.password'
			},
			phone_number:{
				required:true,
				phone_number:true,//自定义的规则
				digits:true,//整数
			}
		},
		//错误信息提示
		messages:{
			username:{
				required:"必须填写用户名",
				minlength:"用户名至少为6个字符",
				maxlength:"用户名至多为20个字符",
				remote: "用户名已存在",
			},
			password:{
				required:"必须填写密码",
				minlength:"密码至少为6个字符",
				maxlength:"密码至多为20个字符",
			},
			email:{
				required:"请输入邮箱地址",
				email: "请输入正确的邮箱地址"
			},
			confirm_password:{
				required: "请再次输入密码",
				minlength: "确认密码不能少于6个字符",
				equalTo: "两次输入密码不一致",//与另一个元素相同
			},
			phone_number:{
				required:"请输入联系方式",
				digits:"*请输入正确的联系方式",
			},
		
		},
	});
	//添加自定义验证规则
	jQuery.validator.addMethod("phone_number", function(value, element) { 
		var length = value.length;
		var phone_number = /^[1][3,4,5,6,7,8,9][0-9]{9}$/;
		return this.optional(element) || (length == 11 && phone_number.test(value)); 
	}, "手机号码格式错误"); 
	//设置表单验证
	$("#setupForm").validate({
		rules:{
			username:{
				required:true,//必填
				minlength:6, //最少6个字符
				maxlength:20,//最多20个字符
				remote:{
					url:"http://kouss.com/demo/Sharelink/remote.json",//用户名重复检查，别跨域调用
					type:"post",
				},
			},
			password:{
				required:true,
				minlength:6, 
				maxlength:20,
			},
			email:{
				required:true,
				email:true,
			},
			confirm_password:{
				required:true,
				minlength:6,
				equalTo:'.password'
			},
			phone_number:{
				required:true,
				phone_number:true,//自定义的规则
				digits:true,//整数
			}
		},
		//错误信息提示
		messages:{
			username:{
				required:"必须填写用户名",
				minlength:"用户名至少为6个字符",
				maxlength:"用户名至多为20个字符",
				remote: "用户名已存在",
			},
			password:{
				required:"必须填写密码",
				minlength:"密码至少为6个字符",
				maxlength:"密码至多为20个字符",
			},
			email:{
				required:"请输入邮箱地址",
				email: "请输入正确的邮箱地址"
			},
			confirm_password:{
				required: "请再次输入密码",
				minlength: "确认密码不能少于6个字符",
				equalTo: "两次输入密码不一致",//与另一个元素相同
			},
			phone_number:{
				required:"请输入联系方式",
				digits:"*请输入正确的联系方式",
			},
		
		},
	});
	//添加自定义验证规则
	jQuery.validator.addMethod("phone_number", function(value, element) { 
		var length = value.length; 
		var phone_number = /^[1][3,4,5,6,7,8,9][0-9]{9}$/;
		return this.optional(element) || (length == 11 && phone_number.test(value)); 
	}, "手机号码格式错误"); 
	//重置密码
	$("#resetForm").validate({
		rules:{
			password:{
				required:true,
				minlength:6, 
				maxlength:20,
			},
			confirm_password:{
				required:true,
				minlength:6,
				equalTo:'.password'
			},
			// phone_number:{
			// 	required:true,
			// 	phone_number:true,//自定义的规则
			// 	digits:true,//整数
			// }
		},
		//错误信息提示
		messages:{
			password:{
				required:"必须填写密码",
				minlength:"密码至少为6个字符",
				maxlength:"密码至多为20个字符",
			},
			confirm_password:{
				required: "请再次输入密码",
				minlength: "确认密码不能少于6个字符",
				equalTo: "两次输入密码不一致",//与另一个元素相同
			},
		},
	});
});
