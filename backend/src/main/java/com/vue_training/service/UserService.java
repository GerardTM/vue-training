package com.vue_training.service;

import com.vue_training.dto.CreateUserRequest;
import com.vue_training.dto.UserResponse;
import com.vue_training.entity.User;
import com.vue_training.exception.InvalidCredentialsException;
import com.vue_training.repository.UserRepository;
import java.time.LocalDateTime;
import java.util.List;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

  private final UserRepository userRepository;
  private final PasswordEncoder passwordEncoder;

  public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
    this.userRepository = userRepository;
    this.passwordEncoder = passwordEncoder;
  }

  public List<UserResponse> findAll() {
    return userRepository.findAll().stream().map(this::toResponse).toList();
  }

  public UserResponse create(CreateUserRequest request) {

    if (userRepository.existsByEmail(request.getEmail())) {
      throw new IllegalArgumentException("Email already exists");
    }

    User user = new User();

    user.setEmail(request.getEmail());
    user.setPassword(passwordEncoder.encode(request.getPassword()));
    user.setFirstName(request.getFirstName());
    user.setLastName(request.getLastName());
    user.setCreatedAt(LocalDateTime.now());

    User savedUser = userRepository.save(user);

    return toResponse(savedUser);
  }

  private UserResponse toResponse(User user) {
    UserResponse response = new UserResponse();

    response.setId(user.getId());
    response.setEmail(user.getEmail());
    response.setFirstName(user.getFirstName());
    response.setLastName(user.getLastName());
    response.setCreatedAt(user.getCreatedAt());

    return response;
  }

  public UserResponse findByEmail(String email) {
    User user = userRepository.findByEmail(email).orElseThrow(InvalidCredentialsException::new);

    return toResponse(user);
  }
}
