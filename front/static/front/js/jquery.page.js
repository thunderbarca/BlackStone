	var aa;
	window.addEventListener('popstate', function () {
        var currentUrl010 = decodeURI(window.location.href); //获取当前链接
        var arr010 = currentUrl010.split("?");
		if(arr010[1]!=parseInt($('#dang').text())){
			$('#tiao').val(arr010[1]);
			 setTimeout(function () {
                $("#zhuan").click()
            },10);
		}
    });
(function($){
	var ms = {
		init:function(obj,args){
			return (function(){
				ms.fillHtml(obj,args);
				ms.bindEvent(obj,args);
			})();
		},
		//填充html
		fillHtml:function(obj,args){
			return (function(){
				obj.empty();
				if(args.current > 1){
					obj.append('<a href="javascript:;" style="font-size: 12px"  class="prevPage0">首页</a>');
				}else{
					obj.append('<a href="javascript:;" style="font-size: 12px;display: none" class="prevPage0">首页</a>');
				}
				//上一页
				if(args.current > 1){
					obj.append('<a href="javascript:;" style="font-size: 12px" class="prevPage"><</a>');
				}else{
					obj.remove('.prevPage');
					obj.append('<span class="disabled"><</span>');
				}
				//中间页码
				if(args.current != 1 && args.current >= 4 && args.pageCount != 4){
					obj.append('<a href="javascript:;" class="tcdNumber">'+1+'</a>');
				}
				if(args.current-2 > 2 && args.current <= args.pageCount && args.pageCount > 5){
					obj.append('<span>...</span>');
				}
				var start = args.current -2,end = args.current+2;
				if((start > 1 && args.current < 4)||args.current == 1){
					end++;
				}
				if(args.current > args.pageCount-4 && args.current >= args.pageCount){
					start--;
				}
				for (;start <= end; start++) {
					if(start <= args.pageCount && start >= 1){
						if(start != args.current){
							obj.append('<a href="javascript:;" class="tcdNumber">'+ start +'</a>');
						}else{
							obj.append('<span class="current">'+ start +'</span>');
						}
					}
				}
				if(args.current + 2 < args.pageCount - 1 && args.current >= 1 && args.pageCount > 5){
					obj.append('<span>...</span>');
				}
				if(args.current != args.pageCount && args.current < args.pageCount -2  && args.pageCount != 4){
					obj.append('<a href="javascript:;" class="tcdNumber">'+args.pageCount+'</a>');
				}
				//下一页
				if(args.current < args.pageCount){
					obj.append('<a href="javascript:;" style="font-size: 12px" class="nextPage">></a>');
				}else{
					obj.remove('.nextPage');
					obj.append('<span class="disabled">></span>');
				}
				if(args.current < args.pageCount){
					obj.append('<a href="javascript:;" style="font-size: 12px"  class="prevPage1">尾页</a>');
				}else{
					obj.append('<a href="javascript:;" style="font-size: 12px;display: none" class="prevPage1">尾页</a>');
				}
			})();
		},
		//绑定事件
		bindEvent:function(obj,args){
			return (function(){
				obj.on("click","a.tcdNumber",function(){
					var current = parseInt($(this).text());
					aa=current;
					$('#dang').text(aa);
					$('#tiao').val(aa)
					ms.fillHtml(obj,{"current":current,"pageCount":args.pageCount});
					if(typeof(args.backFn)=="function"){
						args.backFn(current);
					}
				});
				//首页
				obj.on("click","a.prevPage0",function(){
					var current = 1;
					aa=current;
					$('#dang').text(aa);
					$('#tiao').val(aa)
					ms.fillHtml(obj,{"current":current,"pageCount":args.pageCount});
					if(typeof(args.backFn)=="function"){
						args.backFn(current);
					}
				});
				//上一页
				obj.on("click","a.prevPage",function(){
					var current = parseInt(obj.children("span.current").text());
					aa=current-1;
					$('#dang').text(aa);
					$('#tiao').val(aa)
					bian(aa);
					ms.fillHtml(obj,{"current":current-1,"pageCount":args.pageCount});
					if(typeof(args.backFn)=="function"){
						args.backFn(current-1);
					}
				});
				//下一页
				obj.on("click","a.nextPage",function(){
					var current = parseInt(obj.children("span.current").text());
					aa=current+1;
					$('#dang').text(aa);
					$('#tiao').val(aa)
					ms.fillHtml(obj,{"current":current+1,"pageCount":args.pageCount});
					if(typeof(args.backFn)=="function"){
						args.backFn(current+1);
					}
				});
				//末页
				obj.on("click","a.prevPage1",function(){
					var current = ye;
					aa=current;
					$('#dang').text(aa);
					$('#tiao').val(aa)
					ms.fillHtml(obj,{"current":current,"pageCount":args.pageCount});
					if(typeof(args.backFn)=="function"){
						args.backFn(current);
					}
				});
				//跳转
				$("#zhuan").click(function () {
					var tiao="";
					tiao=$('#tiao').val();
					if($('#tiao').val()>ye){
						tiao=ye;
						$('#tiao').val(ye);
					}
					else if($('#tiao').val()<1){
						tiao=1;
						$('#tiao').val("1");
					}
					else{
						tiao=tiao;
					}
					$(".current").remove('.current');
					obj.append('<span style="display:none" href="javascript:;" class="current">'+tiao+'</span>');
					var current = parseInt(obj.children("span.current").text());
					//console.log(current);
					//var current=tiao;
					aa=current;
					$('#dang').text(aa);
					$('#tiao').val(aa)
					//console.log(aa);
					ms.fillHtml(obj,{"current":current,"pageCount":args.pageCount});
					if(typeof(args.backFn)=="function"){
						args.backFn(current);
					}
				})
			})();
		}
	}
	$.fn.createPage = function(options){
		var args = $.extend({
			pageCount : 10,
			current : 1,
			backFn : function(){}
		},options);
		ms.init(this,args);
	}
})(jQuery);
