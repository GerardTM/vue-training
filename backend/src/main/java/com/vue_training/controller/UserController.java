package com.vue_training.controller;

import com.vue_training.dto.CreateUserRequest;
import com.vue_training.dto.UserResponse;
import com.vue_training.service.UserService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {

  private final UserService userService;

  public UserController(UserService userService) {
    this.userService = userService;
  }

  @GetMapping
  public List<UserResponse> findAll() {
    return userService.findAll();
  }

  @PostMapping
  public UserResponse create(@Valid @RequestBody CreateUserRequest request) {
    return userService.create(request);
  }

  @GetMapping("/me")
  public UserResponse me(Authentication authentication) {
    String email = authentication.getName();

    return userService.findByEmail(email);
  }
}
