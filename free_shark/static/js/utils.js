function InputField(dom,checkFunc=undefined,before_update=undefined,update_callback=undefined,invalid_class="is-invalid",invalid_feedback_class="invalid-feedback",valid_class="is-valid",valid_feedback_class="valid-feedback"){
    dom=$(dom);
    var invalid_feedback=dom.siblings().filter("."+invalid_feedback_class);
    if(!invalid_feedback.length){
        invalid_feedback=$(document.createElement("div"));
        invalid_feedback.addClass(invalid_feedback_class);
        dom.after(invalid_feedback);
    }
    var valid_feedback=dom.siblings().filter("."+valid_feedback_class);
    if(!valid_feedback.length){
        valid_feedback=$(document.createElement("div"));
        valid_feedback.addClass(valid_feedback_class);
        dom.after(valid_feedback);
    }
    d={
        dom:dom,
        update_callback:update_callback,
        before_update:before_update,
        invalid_feedback:invalid_feedback,
        valid_feedback:valid_feedback,
        valid_class:valid_class,
        invalid_class:invalid_class,
        setError:function(message=""){
            dom.addClass(invalid_class).removeClass(valid_class);
            invalid_feedback.text(message);
        },
        clearError:function(){
            dom.removeClass(invalid_class);
        },
        setPass:function(message=""){
            dom.addClass(valid_class).removeClass(invalid_class);
            valid_feedback.text(message);
        },
        clearPass:function(){
            dom.removeClass(valid_class);
        },
        clear:function(){
            this.clearPass();
            this.clearError();
        },
        isInvalid:function(){
            return dom.hasClass(invalid_class);
        },
        isValid:function(){
            return dom.hasClass(valid_class);
        },
        isNormal:function(){
            return !this.isInvalid()&&!this.isValid();
        },
        isNonInvalid:function(){
            return this.isNormal()||this.isValid();
        },
        val:function(){
            return dom.val();
        },
        checkFunc:checkFunc?_.debounce(checkFunc,200):undefined,
        checkFuncDebounce:undefined,
    };
    d.checkFuncDebounce=function(){
        if(this.before_update)
            this.before_update();
        if(this.checkFunc){
            this.checkFunc.bind(this);
            this.checkFunc();
        }
    }
    d.checkFuncDebounce=d.checkFuncDebounce.bind(d);
    dom.on("input",d.checkFuncDebounce);
    return d
}