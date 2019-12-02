/*
 Navicat Premium Data Transfer

 Source Server         : free_shark
 Source Server Type    : MySQL
 Source Server Version : 50645
 Source Host           : localhost:3306
 Source Schema         : free_shark

 Target Server Type    : MySQL
 Target Server Version : 50645
 File Encoding         : 65001

 Date: 01/12/2019 13:47:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for commodity
-- ----------------------------
DROP TABLE IF EXISTS `commodity`;
CREATE TABLE `commodity`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commodity_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '商品名称',
  `commodity_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '商品种类',
  `owner_student_id` int(11) NOT NULL,
  `price` decimal(10, 2) NOT NULL COMMENT '商品价格',
  `commodity_introduction` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品介绍',
  `commodity_photo_url1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图1',
  `commodity_photo_url2` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图2',
  `commodity_photo_url3` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图3',
  `commodity_photo_url4` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图4',
  `commodity_photo_url5` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图5',
  `create_time` datetime(0) NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `owner_student_id`(`owner_student_id`) USING BTREE,
  CONSTRAINT `owner_student_id` FOREIGN KEY (`owner_student_id`) REFERENCES `student` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;


