Feature: Creating a message

  As a support engineer
  I want error messages in RabbitMQ to come off the queue
  So that they are safely stored awaiting review

  Background:
    Given RabbitMQ is running

  Scenario: Errored AMQP message is saved to the knifewrench database
    Given I am authorised to talk to the API
    When a message is published to the error queue
    And 2 seconds have passed
    Then I see that the message has been saved
    And I can look up the message by UUID

  Scenario: Test AMQP message is saved to the knifewrench database
    Given I am authorised to talk to the API
    When I publish a test message with a string body to the error queue
    And 2 seconds have passed
    Then I see that the message has been saved
    And I can look up the message by UUID

  Scenario: Republishing errored AMQP message
    Given I am authorised to talk to the API
    And an errored AMQP message is in knifewrench
    When I republish the AMQP message
    And 2 seconds have passed
    Then I see that the message has been published to rabbitmq
