package com.vue_training.service;

import com.vue_training.dto.LoginRequest;
import com.vue_training.dto.LoginResponse;
import com.vue_training.dto.UserResponse;
import com.vue_training.entity.User;
import com.vue_training.exception.InvalidCredentialsException;
import com.vue_training.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class LoginService {

  private final UserRepository userRepository;
  private final PasswordEncoder passwordEncoder;
  private final JwtService jwtService;

  public LoginService(
      UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
    this.userRepository = userRepository;
    this.passwordEncoder = passwordEncoder;
    this.jwtService = jwtService;
  }

  public LoginResponse login(LoginRequest request) {

    User user =
        userRepository
            .findByEmail(request.getEmail())
            .orElseThrow(InvalidCredentialsException::new);

    if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
      throw new InvalidCredentialsException();
    }

    String token = jwtService.generateToken(user.getId(), user.getEmail());

    return new LoginResponse(token, toResponse(user));
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
}
