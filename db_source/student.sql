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

 Date: 01/12/2019 13:48:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `school_number` varchar(0) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '学号，可以从邮箱里取',
  `real_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `college` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '学院',
  `class` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '班级',
  `contact` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '可以是微信，QQ或者电话',
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
