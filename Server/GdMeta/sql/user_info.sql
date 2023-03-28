/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50521
Source Host           : localhost:3306
Source Database       : gdmeta

Target Server Type    : MYSQL
Target Server Version : 50521
File Encoding         : 65001

Date: 2023-02-24 18:49:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `user_info`
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(128) NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(128) NOT NULL DEFAULT '' COMMENT '用户密码',
  `telephonenum` varchar(32) NOT NULL DEFAULT '' COMMENT '电话号码',
  `sex` int(11) NOT NULL DEFAULT '1' COMMENT '1:男性，2:女性',
  `status` int(11) NOT NULL DEFAULT '1' COMMENT '1:正常的，0:删除的',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_info
-- ----------------------------
