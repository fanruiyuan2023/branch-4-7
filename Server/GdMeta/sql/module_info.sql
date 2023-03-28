/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50521
Source Host           : localhost:3306
Source Database       : gdmeta

Target Server Type    : MYSQL
Target Server Version : 50521
File Encoding         : 65001

Date: 2023-02-24 18:49:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `module_info`
-- ----------------------------
DROP TABLE IF EXISTS `module_info`;
CREATE TABLE `module_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID号',
  `author` varchar(64) DEFAULT '' COMMENT '作者',
  `title` varchar(128) DEFAULT '' COMMENT '标题',
  `image` varchar(256) DEFAULT '' COMMENT '图片路径',
  `modele` varchar(256) DEFAULT '' COMMENT '模型名称',
  `desp` varchar(128) DEFAULT '' COMMENT '作品描述',
  `upload_date` datetime DEFAULT NULL COMMENT '上传日期',
  `status` int(11) DEFAULT '1' COMMENT '1:合法的，0:删除的',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of module_info
-- ----------------------------
