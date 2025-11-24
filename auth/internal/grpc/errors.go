package auth

import (
	"errors"

	"github.com/IvanDrf/auth/internal/errs"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func handleRegisterError(err error) error {
	if errors.Is(err, errs.ErrInvalidEmail()) {
		return status.Error(codes.InvalidArgument, err.Error())
	}

	if errors.Is(err, errs.ErrUserAlreadyInDB()) {
		return status.Error(codes.Canceled, err.Error())
	}

	if errors.Is(err, errs.ErrCantAddNewUser()) {
		return status.Error(codes.Internal, err.Error())
	}

	if errors.Is(err, errs.ErrCantCreateVerifToken()) {
		return status.Error(codes.Internal, err.Error())
	}

	if errors.Is(err, errs.ErrCantSaveVerifToken()) {
		return status.Error(codes.Internal, err.Error())
	}

	return nil
}

func handleLoginError(err error) error {
	if errors.Is(err, errs.ErrCantFindUserInDB()) {
		return status.Error(codes.Unauthenticated, err.Error())
	}

	if errors.Is(err, errs.ErrIncorrectPassword()) {
		return status.Error(codes.InvalidArgument, err.Error())
	}

	if errors.Is(err, errs.ErrCantCreateJWT()) {
		return status.Error(codes.Internal, err.Error())
	}

	return nil
}
