#ifndef MODULES_BASIC_DS_TENSOR_VINEYARD_H
#define MODULES_BASIC_DS_TENSOR_VINEYARD_H

/** Copyright 2020-2023 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef MODULES_BASIC_DS_TENSOR_VINEYARD_MOD_
#define MODULES_BASIC_DS_TENSOR_VINEYARD_MOD_

#include <algorithm>
#include <functional>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "arrow/api.h"
#include "arrow/io/api.h"

#include "basic/ds/array.vineyard.h"
#include "basic/ds/arrow.h"
#include "basic/ds/arrow.vineyard.h"
#include "basic/ds/types.h"
#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/json.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

namespace detail {

template <typename T>
struct ArrowTensorType {
  using type = arrow::NumericTensor<typename arrow::CTypeTraits<T>::ArrowType>;
};

template <>
struct ArrowTensorType<arrow_string_view> {
  using type = void;
};

}  // namespace detail

template <typename T>
class TensorBaseBuilder;

class ITensor : public Object {
 public:
  __attribute__((annotate("shared"))) virtual std::vector<int64_t> const& shape() const = 0;

  __attribute__((annotate("shared"))) virtual std::vector<int64_t> const& partition_index() const = 0;

  __attribute__((annotate("shared"))) virtual AnyType value_type() const = 0;

  __attribute__((annotate("shared"))) virtual const std::shared_ptr<arrow::Buffer> buffer() const = 0;

  __attribute__((annotate("shared"))) virtual const std::shared_ptr<arrow::Buffer> auxiliary_buffer()
      const = 0;
};

template <typename T>
class __attribute__((annotate("vineyard"))) Tensor : public ITensor, public BareRegistered<Tensor<T>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Tensor<T>>{
                new Tensor<T>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Tensor<T>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("value_type_", this->value_type_);
        this->buffer_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_"));
        meta.GetKeyValue("shape_", this->shape_);
        meta.GetKeyValue("partition_index_", this->partition_index_);

        
    }

 private:
public:
  using value_t = T;
  using value_pointer_t = T*;
  using value_const_pointer_t = const T*;
  using ArrowTensorT = typename detail::ArrowTensorType<T>::type;

  /**
   * @brief Get the strides of the tensor.
   *
   * @return The strides of the tensor. The definition of the tensor's strides
   * can be found in https://pytorch.org/docs/stable/tensor_attributes.html
   */
  __attribute__((annotate("shared"))) std::vector<int64_t> strides() const {
    std::vector<int64_t> vec(shape_.size());
    vec[shape_.size() - 1] = sizeof(T);
    for (size_t i = shape_.size() - 1; i > 0; --i) {
      vec[i - 1] = vec[i] * shape_[i];
    }
    return vec;
  }

  /**
   * @brief Get the shape of the tensor.
   *
   * @return The shape vector where the ith element represents
   * the size of the ith axis.
   */
  __attribute__((annotate("shared"))) std::vector<int64_t> const& shape() const override {
    return shape_;
  }

  /**
   * @brief Get the index of this partition in the global tensor.
   *
   * @return The index vector where the ith element represents the index
   * in the ith axis.
   */
  __attribute__((annotate("shared"))) std::vector<int64_t> const& partition_index() const override {
    return partition_index_;
  }

  /**
   * @brief Get the type of tensor's elements.
   *
   * @return The type of the tensor's elements.
   */
  __attribute__((annotate("shared"))) AnyType value_type() const override { return this->value_type_; }

  /**
   * @brief Get the data pointer to the tensor's data buffer.
   *
   * @return The data pointer.
   */
  __attribute__((annotate("shared"))) value_const_pointer_t data() const {
    return reinterpret_cast<const T*>(buffer_->data());
  }

  /**
   * @brief Get the data in the tensor by index.
   *
   * @return The data reference.
   */
  __attribute__((annotate("shared"))) const value_t operator[](size_t index) const {
    return this->data()[index];
  }

  /**
   * @brief Get the buffer of the tensor.
   *
   * @return The shared pointer to an arrow buffer which
   * holds the data buffer of the tensor.
   */
  __attribute__((annotate("shared"))) const std::shared_ptr<arrow::Buffer> buffer() const override {
    return this->buffer_->ArrowBuffer();
  }

  __attribute__((annotate("shared"))) const std::shared_ptr<arrow::Buffer> auxiliary_buffer()
      const override {
    return nullptr;
  }

  /**
   * @brief Return a view of the original tensor so that it can be used as
   * arrow's Tensor.
   *
   */
  __attribute__((annotate("shared"))) const std::shared_ptr<ArrowTensorT> ArrowTensor() {
    return std::make_shared<ArrowTensorT>(buffer_->ArrowBuffer(), shape());
  }

 private:
  __attribute__((annotate("shared"))) AnyType value_type_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_;
  __attribute__((annotate("shared"))) Tuple<int64_t> shape_;
  __attribute__((annotate("shared"))) Tuple<int64_t> partition_index_;

  friend class Client;
  friend class TensorBaseBuilder<T>;
};

template <>
class __attribute__((annotate("vineyard"))) Tensor<std::string>
    : public ITensor, public BareRegistered<Tensor<std::string>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Tensor<std::string>>{
                new Tensor<std::string>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Tensor<std::string>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("value_type_", this->value_type_);
        this->buffer_ = std::dynamic_pointer_cast<LargeStringArray>(meta.GetMember("buffer_"));
        meta.GetKeyValue("shape_", this->shape_);
        meta.GetKeyValue("partition_index_", this->partition_index_);

        
    }

 private:
public:
  using value_t = arrow_string_view;
  using value_pointer_t = uint8_t*;
  using value_const_pointer_t = const uint8_t*;
  using ArrowTensorT =
      typename detail::ArrowTensorType<arrow_string_view>::type;

  /**
   * @brief Get the strides of the tensor.
   *
   * @return The strides of the tensor. The definition of the tensor's strides
   * can be found in https://pytorch.org/docs/stable/tensor_attributes.html
   */
  __attribute__((annotate("shared"))) std::vector<int64_t> strides() const {
    std::vector<int64_t> vec(shape_.size());
    vec[shape_.size() - 1] = 1 /* special case for tensors */;
    for (size_t i = shape_.size() - 1; i > 0; --i) {
      vec[i - 1] = vec[i] * shape_[i];
    }
    return vec;
  }

  /**
   * @brief Get the shape of the tensor.
   *
   * @return The shape vector where the ith element represents
   * the size of the ith axis.
   */
  __attribute__((annotate("shared"))) std::vector<int64_t> const& shape() const override {
    return shape_;
  }

  /**
   * @brief Get the index of this partition in the global tensor.
   *
   * @return The index vector where the ith element represents the index
   * in the ith axis.
   */
  __attribute__((annotate("shared"))) std::vector<int64_t> const& partition_index() const override {
    return partition_index_;
  }

  /**
   * @brief Get the type of tensor's elements.
   *
   * @return The type of the tensor's elements.
   */
  __attribute__((annotate("shared"))) AnyType value_type() const override { return this->value_type_; }

  /**
   * @brief Get the data pointer to the tensor's data buffer.
   *
   * @return The data pointer.
   */
  __attribute__((annotate("shared"))) value_const_pointer_t data() const {
    return this->buffer_->GetArray()->raw_data();
  }

  /**
   * @brief Get the data in the tensor by index.
   *
   * @return The data reference.
   */
  __attribute__((annotate("shared"))) const value_t operator[](size_t index) const {
    return this->buffer_->GetArray()->GetView(index);
  }

  /**
   * @brief Get the buffer of the tensor.
   *
   * @return The shared pointer to an arrow buffer which
   * holds the data buffer of the tensor.
   */
  __attribute__((annotate("shared"))) const std::shared_ptr<arrow::Buffer> buffer() const override {
    return this->buffer_->GetArray()->value_data();
  }

  /**
   * @brief Get the buffer of the tensor.
   *
   * @return The shared pointer to an arrow buffer which
   * holds the data buffer of the tensor.
   */
  __attribute__((annotate("shared"))) const std::shared_ptr<arrow::Buffer> auxiliary_buffer()
      const override {
    return this->buffer_->GetArray()->value_data();
  }

  /**
   * @brief Return a view of the original tensor so that it can be used as
   * arrow's Tensor.
   *
   */
  __attribute__((annotate("shared"))) const std::shared_ptr<ArrowTensorT> ArrowTensor() {
    // No corresponding arrow tensor type for std::string.
    return nullptr;
  }

 private:
  __attribute__((annotate("shared"))) AnyType value_type_;
  __attribute__((annotate("shared"))) std::shared_ptr<LargeStringArray> buffer_;
  __attribute__((annotate("shared"))) Tuple<int64_t> shape_;
  __attribute__((annotate("shared"))) Tuple<int64_t> partition_index_;

  friend class Client;
  friend class TensorBaseBuilder<std::string>;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_TENSOR_VINEYARD_MOD_

// vim: syntax=cpp

namespace vineyard {

template<typename T>
class TensorBaseBuilder: public ObjectBuilder {
  public:
    // using value_t
    using value_t = T;
    // using value_pointer_t
    using value_pointer_t = T*;
    // using value_const_pointer_t
    using value_const_pointer_t = const T*;
    // using ArrowTensorT
    using ArrowTensorT = typename detail::ArrowTensorType<T>::type;

    explicit TensorBaseBuilder(Client &client) {}

    explicit TensorBaseBuilder(
            Tensor<T> const &__value) {
        this->set_value_type_(__value.value_type_);
        this->set_buffer_(__value.buffer_);
        this->set_shape_(__value.shape_);
        this->set_partition_index_(__value.partition_index_);
    }

    explicit TensorBaseBuilder(
            std::shared_ptr<Tensor<T>> const & __value):
        TensorBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<Tensor<T>> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<Tensor<T>>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Tensor<T>>());

        __value->value_type_ = value_type_;
        __value->meta_.AddKeyValue("value_type_", __value->value_type_);

        // using __buffer__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer__value_type = typename decltype(__value->buffer_)::element_type;
        auto __value_buffer_ = std::dynamic_pointer_cast<__buffer__value_type>(
            buffer_->_Seal(client));
        __value->buffer_ = __value_buffer_;
        __value->meta_.AddMember("buffer_", __value->buffer_);
        __value_nbytes += __value_buffer_->nbytes();

        __value->shape_ = shape_;
        __value->meta_.AddKeyValue("shape_", __value->shape_);

        __value->partition_index_ = partition_index_;
        __value->meta_.AddKeyValue("partition_index_", __value->partition_index_);

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    AnyType value_type_;
    std::shared_ptr<ObjectBase> buffer_;
    Tuple<int64_t> shape_;
    Tuple<int64_t> partition_index_;

    void set_value_type_(AnyType const &value_type__) {
        this->value_type_ = value_type__;
    }

    void set_buffer_(std::shared_ptr<ObjectBase> const & buffer__) {
        this->buffer_ = buffer__;
    }

    void set_shape_(Tuple<int64_t> const &shape__) {
        this->shape_ = shape__;
    }

    void set_partition_index_(Tuple<int64_t> const &partition_index__) {
        this->partition_index_ = partition_index__;
    }

  private:
    friend class Tensor<T>;
};


}  // namespace vineyard




namespace vineyard {

template <>
class TensorBaseBuilder<std::string>: public ObjectBuilder {
  public:
    // using value_t
    using value_t = arrow_string_view;
    // using value_pointer_t
    using value_pointer_t = uint8_t*;
    // using value_const_pointer_t
    using value_const_pointer_t = const uint8_t*;
    // using ArrowTensorT
    using ArrowTensorT =
      typename detail::ArrowTensorType<arrow_string_view>::type;

    explicit TensorBaseBuilder(Client &client) {}

    explicit TensorBaseBuilder(
            Tensor<std::string> const &__value) {
        this->set_value_type_(__value.value_type_);
        this->set_buffer_(__value.buffer_);
        this->set_shape_(__value.shape_);
        this->set_partition_index_(__value.partition_index_);
    }

    explicit TensorBaseBuilder(
            std::shared_ptr<Tensor<std::string>> const & __value):
        TensorBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<Tensor<std::string>> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<Tensor<std::string>>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Tensor<std::string>>());

        __value->value_type_ = value_type_;
        __value->meta_.AddKeyValue("value_type_", __value->value_type_);

        // using __buffer__value_type = typename std::shared_ptr<LargeStringArray>::element_type;
        using __buffer__value_type = typename decltype(__value->buffer_)::element_type;
        auto __value_buffer_ = std::dynamic_pointer_cast<__buffer__value_type>(
            buffer_->_Seal(client));
        __value->buffer_ = __value_buffer_;
        __value->meta_.AddMember("buffer_", __value->buffer_);
        __value_nbytes += __value_buffer_->nbytes();

        __value->shape_ = shape_;
        __value->meta_.AddKeyValue("shape_", __value->shape_);

        __value->partition_index_ = partition_index_;
        __value->meta_.AddKeyValue("partition_index_", __value->partition_index_);

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    AnyType value_type_;
    std::shared_ptr<ObjectBase> buffer_;
    Tuple<int64_t> shape_;
    Tuple<int64_t> partition_index_;

    void set_value_type_(AnyType const &value_type__) {
        this->value_type_ = value_type__;
    }

    void set_buffer_(std::shared_ptr<ObjectBase> const & buffer__) {
        this->buffer_ = buffer__;
    }

    void set_shape_(Tuple<int64_t> const &shape__) {
        this->shape_ = shape__;
    }

    void set_partition_index_(Tuple<int64_t> const &partition_index__) {
        this->partition_index_ = partition_index__;
    }

  private:
    friend class Tensor<std::string>;
};


}  // namespace vineyard



#endif // MODULES_BASIC_DS_TENSOR_VINEYARD_H
