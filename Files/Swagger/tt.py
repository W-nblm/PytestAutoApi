{
    "path": "/mqtt/VirtualDeviceTest/unbind",
    "method": "POST",
    "summary": "解绑设备同时",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不 用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/startAi",
    "method": "POST",
    "summary": "给设备生成birdAI事件",
    "parameters": {
        "content": {
            "application/json": {
                "schema": {
                    "required": ["devId", "picurl"],
                    "type": "object",
                    "properties": {
                        "devId": {"type": "string"},
                        "picurl": {"type": "string"},
                        "picHDurl": {"type": "string"},
                        "birdAiName": {"type": "string"},
                        "scorce": {"type": "number", "format": "float"},
                    },
                    "description": "",
                }
            }
        },
        "required": True,
    },
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提 示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "boolean", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/sendShadowCommand",
    "method": "POST",
    "summary": "向影子设备发送请求",
    "parameters": {
        "content": {
            "application/json": {
                "schema": {
                    "required": ["data", "devId", "productId"],
                    "type": "object",
                    "properties": {
                        "devId": {"type": "string", "description": "目标设备id"},
                        "productId": {"type": "string", "description": "产品id"},
                        "homeId": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "userId": {"type": "string"},
                                "code": {"type": "string"},
                                "value": {
                                    "type": "object",
                                    "description": "具体指令值",
                                },
                            },
                            "description": "user: xiehui\n date: 2023/2/20",
                        },
                    },
                    "description": "user: xiehui\n date: 2023/3/25",
                }
            }
        },
        "required": True,
    },
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message  仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/sendRealTimeProperty",
    "method": "POST",
    "summary": "向设备下发获取属性",
    "parameters": {
        "content": {
            "application/json": {
                "schema": {
                    "required": ["data", "devId", "productId"],
                    "type": "object",
                    "properties": {
                        "devId": {"type": "string", "description": "目标设备id"},
                        "productId": {"type": "string", "description": "产品id"},
                        "homeId": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "userId": {"type": "string"},
                                "code": {"type": "string"},
                            },
                            "description": "user: xiehui\n date: 2023/3/25",
                        },
                    },
                    "description": "user: xiehui\n date: 2023/3/25",
                }
            }
        },
        "required": True,
    },
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {
                                "type": "object",
                                "properties": {
                                    "requestId": {
                                        "type": "string",
                                        "description": "请求id",
                                    },
                                    "isLink": {"type": "boolean"},
                                    "msg": {"type": "string"},
                                    "succ": {"type": "boolean"},
                                },
                                "description": "user: xiehui\n date: 2023/3/25",
                            },
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/sendRealTimeCommand",
    "method": "POST",
    "summary": "向设备下发实时命令",
    "parameters": {
        "content": {
            "application/json": {
                "schema": {
                    "required": ["data", "devId", "productId"],
                    "type": "object",
                    "properties": {
                        "devId": {"type": "string", "description": "目标设备id"},
                        "productId": {"type": "string", "description": "产品id"},
                        "homeId": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "userId": {"type": "string"},
                                "code": {"type": "string"},
                                "value": {
                                    "type": "object",
                                    "description": "具体指令值",
                                },
                            },
                            "description": "user: xiehui\n date: 2023/2/20",
                        },
                    },
                    "description": "user: xiehui\n date: 2023/3/25",
                }
            }
        },
        "required": True,
    },
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {
                                "type": "object",
                                "properties": {
                                    "requestId": {
                                        "type": "string",
                                        "description": "请求id",
                                    },
                                    "isLink": {"type": "boolean"},
                                    "msg": {"type": "string"},
                                    "succ": {"type": "boolean"},
                                },
                                "description": "user: xiehui\n date: 2023/3/25",
                            },
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/reboot",
    "method": "POST",
    "summary": "重启设备",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/queryVirtualDevList",
    "method": "POST",
    "summary": "查询虚拟设备列表",
    "parameters": {
        "content": {
            "application/json": {
                "schema": {
                    "required": ["devId", "productId"],
                    "type": "object",
                    "properties": {
                        "devId": {"type": "string", "description": "设备id"},
                        "productId": {"type": "string", "description": "产品id"},
                    },
                    "description": "系统用户创建虚拟设备的关系业务对象 device_user_virtual_ship",
                }
            }
        },
        "required": True,
    },
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {
                                "type": "array",
                                "description": "数据对象",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "format": "int64"},
                                        "devId": {
                                            "type": "string",
                                            "description": "设备id",
                                        },
                                        "userId": {
                                            "type": "string",
                                            "description": "系统用户id",
                                        },
                                        "productId": {
                                            "type": "string",
                                            "description": "产品id",
                                        },
                                    },
                                    "description": "系统用户创建虚拟设备的关系视图对象 device_user_virtual_ship",
                                },
                            },
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/heartBeat",
    "method": "GET",
    "summary": "HeartBeat",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470 有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/testSendNtp",
    "method": "GET",
    "summary": "模拟设备发送Ntp对时",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/testSendNetwork",
    "method": "GET",
    "summary": "添加设备同时模拟设备发送配网",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/testGetDevProps",
    "method": "GET",
    "summary": "获取设备所有影子属性",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {
                                "type": "array",
                                "description": "数据对象",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "devId": {
                                            "type": "string",
                                            "description": "设备id",
                                        },
                                        "modelCode": {
                                            "type": "string",
                                            "description": "设备id",
                                        },
                                        "type": {
                                            "type": "string",
                                            "description": "指令类型Boolean, Enum, Integer,Float ,String,Json, Raw",
                                        },
                                        "value": {
                                            "type": "object",
                                            "description": "具体指令值",
                                        },
                                    },
                                    "description": "",
                                },
                            },
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示 例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/setDevActive",
    "method": "GET",
    "summary": "设置某个设备状态为运行",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {"type": "object", "description": "数据对象"},
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}, {
    "path": "/mqtt/VirtualDeviceTest/getExeValue",
    "method": "GET",
    "summary": "获取命令执行异步结果",
    "parameters": {},
    "responses": {
        "200": {
            "description": "OK",
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "description": "消息状态码(470,校验errorcode, 提示msg多语言内容, 500:app直接提示服务异常)",
                                "format": "int32",
                            },
                            "msg": {
                                "type": "string",
                                "description": "消息内容  多语言message 仅状态码470有效, 其他为前端自己多语言",
                            },
                            "data": {
                                "type": "object",
                                "properties": {
                                    "devId": {
                                        "type": "string",
                                        "description": "设备id",
                                    },
                                    "time": {
                                        "type": "integer",
                                        "description": "时间戳",
                                        "format": "int64",
                                    },
                                    "succ": {
                                        "type": "boolean",
                                        "description": "是否成功",
                                    },
                                    "status": {
                                        "type": "integer",
                                        "description": "0：代表命令发送不成功，1，代表命令发送成功，设备处理中，2:代表设备处理完成",
                                        "format": "int32",
                                    },
                                    "msg": {
                                        "type": "string",
                                        "description": "失败后消息提示",
                                    },
                                    "data": {
                                        "type": "object",
                                        "description": "命令执行成功后返回的数据对象",
                                    },
                                },
                                "description": "user: xiehui\n date: 2023/2/11",
                            },
                            "paramMsg": {
                                "type": "object",
                                "additionalProperties": {"type": "object"},
                                "description": '参数校验返回对象(给web使用, app不用)\n 示例: {"字段名": "提示消息"}\n {"userName": "用户名已存在,请重新输入"}',
                            },
                            "errCode": {
                                "type": "integer",
                                "description": "仅状态码470有效校验errorcode",
                                "format": "int32",
                            },
                        },
                        "description": "响应信息主体",
                    }
                }
            },
        }
    },
}
