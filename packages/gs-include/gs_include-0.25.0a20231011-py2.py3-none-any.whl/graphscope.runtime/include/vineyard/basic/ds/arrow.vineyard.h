#ifndef MODULES_BASIC_DS_ARROW_VINEYARD_H
#define MODULES_BASIC_DS_ARROW_VINEYARD_H

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

#ifndef MODULES_BASIC_DS_ARROW_VINEYARD_MOD_
#define MODULES_BASIC_DS_ARROW_VINEYARD_MOD_

#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "arrow/api.h"
#include "arrow/io/api.h"
#include "arrow/ipc/api.h"

#include "basic/ds/arrow_utils.h"
#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/collection.h"
#include "client/ds/core_types.h"
#include "client/ds/stream.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

/// The arrays in vineyard is a wrapper of arrow arrays, in order to
/// Simplify the Build and Construct process.

class ArrowArray {
 public:
  virtual std::shared_ptr<arrow::Array> ToArray() const = 0;
};

namespace detail {
std::shared_ptr<arrow::Array> CastToArray(std::shared_ptr<Object> object);
}  // namespace detail

class FlatArray : public ArrowArray {};

/// Primitive array

/// Base class for primitive arrays for type factory.

class PrimitiveArray : public FlatArray {};

template <typename T>
class NumericArrayBaseBuilder;

template <typename T>
class __attribute__((annotate("vineyard"))) NumericArray : public PrimitiveArray,
                                  public Registered<NumericArray<T>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<NumericArray<T>>{
                new NumericArray<T>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<NumericArray<T>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("length_", this->length_);
        meta.GetKeyValue("null_count_", this->null_count_);
        meta.GetKeyValue("offset_", this->offset_);
        this->buffer_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_"));
        this->null_bitmap_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("null_bitmap_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  using ArrayType = ArrowArrayType<T>;

  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<Blob> GetBuffer() const { return buffer_; }

  std::shared_ptr<ArrayType> GetArray() const { return array_; }

  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }

  const uint8_t* GetBase() const { return array_->values()->data(); }

  const size_t length() const { return array_->length(); }

  const T* raw_values() const { return array_->raw_values(); }

 private:
  __attribute__((annotate("shared"))) size_t length_;
  __attribute__((annotate("shared"))) int64_t null_count_, offset_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_, null_bitmap_;

  std::shared_ptr<ArrayType> array_;
  friend class Client;
  friend class NumericArrayBaseBuilder<T>;
};

using Int8Array = NumericArray<int8_t>;
using Int16Array = NumericArray<int16_t>;
using Int32Array = NumericArray<int32_t>;
using Int64Array = NumericArray<int64_t>;
using UInt8Array = NumericArray<uint8_t>;
using UInt16Array = NumericArray<uint16_t>;
using UInt32Array = NumericArray<uint32_t>;
using UInt64Array = NumericArray<uint64_t>;
using FloatArray = NumericArray<float>;
using DoubleArray = NumericArray<double>;

class BooleanArrayBaseBuilder;

class __attribute__((annotate("vineyard"))) BooleanArray : public PrimitiveArray,
                                  public Registered<BooleanArray> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<BooleanArray>{
                new BooleanArray()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<BooleanArray>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("length_", this->length_);
        meta.GetKeyValue("null_count_", this->null_count_);
        meta.GetKeyValue("offset_", this->offset_);
        this->buffer_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_"));
        this->null_bitmap_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("null_bitmap_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  using ArrayType = ArrowArrayType<bool>;

  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<Blob> GetBuffer() const { return buffer_; }

  std::shared_ptr<ArrayType> GetArray() const { return array_; }

  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }

  const uint8_t* GetBase() const { return array_->values()->data(); }

 private:
  __attribute__((annotate("shared"))) size_t length_;
  __attribute__((annotate("shared"))) int64_t null_count_, offset_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_, null_bitmap_;

  std::shared_ptr<ArrayType> array_;
  friend class Client;
  friend class BooleanArrayBaseBuilder;
};

/// Binary array

template <typename ArrayType>
class BaseBinaryArrayBaseBuilder;

template <typename ArrayType>
class __attribute__((annotate("vineyard"))) BaseBinaryArray
    : public FlatArray,
      public Registered<BaseBinaryArray<ArrayType>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<BaseBinaryArray<ArrayType>>{
                new BaseBinaryArray<ArrayType>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<BaseBinaryArray<ArrayType>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("length_", this->length_);
        meta.GetKeyValue("null_count_", this->null_count_);
        meta.GetKeyValue("offset_", this->offset_);
        this->buffer_data_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_data_"));
        this->buffer_offsets_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_offsets_"));
        this->null_bitmap_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("null_bitmap_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<Blob> GetBuffer() const { return buffer_data_; }

  std::shared_ptr<Blob> GetOffsetsBuffer() const { return buffer_offsets_; }

  std::shared_ptr<ArrayType> GetArray() const { return array_; }

  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }
  const uint8_t* GetBase() const { return array_->value_data()->data(); }

 private:
  __attribute__((annotate("shared"))) size_t length_;
  __attribute__((annotate("shared"))) int64_t null_count_, offset_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_data_, buffer_offsets_, null_bitmap_;

  std::shared_ptr<ArrayType> array_;

  friend class Client;

  friend class BaseBinaryArrayBaseBuilder<ArrayType>;
};

using BinaryArray = BaseBinaryArray<arrow::BinaryArray>;
using LargeBinaryArray = BaseBinaryArray<arrow::LargeBinaryArray>;
using StringArray = BaseBinaryArray<arrow::StringArray>;
using LargeStringArray = BaseBinaryArray<arrow::LargeStringArray>;

class FixedSizeBinaryArrayBaseBuilder;

class __attribute__((annotate("vineyard"))) FixedSizeBinaryArray
    : public PrimitiveArray,
      public Registered<FixedSizeBinaryArray> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<FixedSizeBinaryArray>{
                new FixedSizeBinaryArray()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<FixedSizeBinaryArray>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("byte_width_", this->byte_width_);
        meta.GetKeyValue("length_", this->length_);
        meta.GetKeyValue("null_count_", this->null_count_);
        meta.GetKeyValue("offset_", this->offset_);
        this->buffer_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_"));
        this->null_bitmap_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("null_bitmap_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<Blob> GetBuffer() const { return buffer_; }

  std::shared_ptr<arrow::FixedSizeBinaryArray> GetArray() const {
    return array_;
  }
  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }

 private:
  __attribute__((annotate("shared"))) int32_t byte_width_;
  __attribute__((annotate("shared"))) size_t length_;
  __attribute__((annotate("shared"))) int64_t null_count_, offset_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_, null_bitmap_;

  std::shared_ptr<arrow::FixedSizeBinaryArray> array_;

  friend class Client;
  friend class FixedSizeBinaryArrayBaseBuilder;
};

/// Null array

class NullArrayBaseBuilder;

class __attribute__((annotate("vineyard"))) NullArray : public FlatArray, public Registered<NullArray> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<NullArray>{
                new NullArray()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<NullArray>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("length_", this->length_);

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  using ArrayType = arrow::NullArray;
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<Blob> GetBuffer() const { return nullptr; }

  std::shared_ptr<ArrayType> GetArray() const { return array_; }

  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }

 private:
  __attribute__((annotate("shared"))) size_t length_;

  std::shared_ptr<arrow::NullArray> array_;

  friend class Client;
  friend class NullArrayBaseBuilder;
};

/// Nested array

template <typename ArrayType>
class BaseListArrayBaseBuilder;

template <typename ArrayType>
class __attribute__((annotate("vineyard"))) BaseListArray : public ArrowArray,
                                   public Registered<BaseListArray<ArrayType>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<BaseListArray<ArrayType>>{
                new BaseListArray<ArrayType>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<BaseListArray<ArrayType>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("length_", this->length_);
        meta.GetKeyValue("null_count_", this->null_count_);
        meta.GetKeyValue("offset_", this->offset_);
        this->buffer_offsets_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_offsets_"));
        this->null_bitmap_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("null_bitmap_"));
        this->values_ = std::dynamic_pointer_cast<Object>(meta.GetMember("values_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<ArrayType> GetArray() const { return array_; }

  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }

  std::shared_ptr<arrow::Array> GetBase() const { return array_->values(); }

 private:
  __attribute__((annotate("shared"))) size_t length_;
  __attribute__((annotate("shared"))) int64_t null_count_, offset_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_offsets_, null_bitmap_;
  __attribute__((annotate("shared"))) std::shared_ptr<Object> values_;

  std::shared_ptr<ArrayType> array_;

  friend class Client;
  friend class BaseListArrayBaseBuilder<ArrayType>;
};

using ListArray = BaseListArray<arrow::ListArray>;
using LargeListArray = BaseListArray<arrow::LargeListArray>;

class FixedSizeListArrayBaseBuilder;

class __attribute__((annotate("vineyard"))) FixedSizeListArray : public ArrowArray,
                                        public Registered<FixedSizeListArray> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<FixedSizeListArray>{
                new FixedSizeListArray()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<FixedSizeListArray>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("length_", this->length_);
        meta.GetKeyValue("list_size_", this->list_size_);
        this->values_ = std::dynamic_pointer_cast<Object>(meta.GetMember("values_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<arrow::FixedSizeListArray> GetArray() const { return array_; }

  std::shared_ptr<arrow::Array> ToArray() const override { return array_; }

  const uint8_t* GetBase() const {
    return array_->values()->data()->buffers[1]->data();
  }

 private:
  __attribute__((annotate("shared"))) size_t length_;
  __attribute__((annotate("shared"))) size_t list_size_;
  __attribute__((annotate("shared"))) std::shared_ptr<Object> values_;

  std::shared_ptr<arrow::FixedSizeListArray> array_;

  friend class Client;
  friend class FixedSizeListArrayBaseBuilder;
};

class SchemaProxyBaseBuilder;

class __attribute__((annotate("vineyard"))) SchemaProxy : public Registered<SchemaProxy> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<SchemaProxy>{
                new SchemaProxy()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<SchemaProxy>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("schema_textual_", this->schema_textual_);
        meta.GetKeyValue("schema_binary_", this->schema_binary_);

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<arrow::Schema> const& GetSchema() const { return schema_; }

 private:
  __attribute__((annotate("shared"))) json schema_textual_;
  __attribute__((annotate("shared"))) json schema_binary_;

  std::shared_ptr<arrow::Schema> schema_;

  friend class Client;
  friend class SchemaProxyBaseBuilder;
};

class RecordBatchBaseBuilder;

class __attribute__((annotate("vineyard(streamable)"))) RecordBatch : public Registered<RecordBatch> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<RecordBatch>{
                new RecordBatch()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<RecordBatch>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        Object::Construct(meta);

        meta.GetKeyValue("column_num_", this->column_num_);
        meta.GetKeyValue("row_num_", this->row_num_);
        this->schema_.Construct(meta.GetMemberMeta("schema_"));
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__columns_-size"); ++__idx) {
            this->columns_.emplace_back(std::dynamic_pointer_cast<Object>(
                    meta.GetMember("__columns_-" + std::to_string(__idx))));
        }

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<arrow::RecordBatch> GetRecordBatch() const;

  std::shared_ptr<arrow::Schema> schema() const { return schema_.GetSchema(); }

  size_t num_columns() const { return column_num_; }

  size_t num_rows() const { return row_num_; }

  std::vector<std::shared_ptr<Object>> const& columns() const {
    return columns_;
  }

  std::vector<std::shared_ptr<arrow::Array>> const& arrow_columns() const {
    return arrow_columns_;
  }

 private:
  __attribute__((annotate("shared"))) size_t column_num_ = 0;
  __attribute__((annotate("shared"))) size_t row_num_ = 0;
  __attribute__((annotate("shared"))) SchemaProxy schema_;
  __attribute__((annotate("shared"))) Tuple<std::shared_ptr<Object>> columns_;

  std::vector<std::shared_ptr<arrow::Array>> arrow_columns_;
  mutable std::shared_ptr<arrow::RecordBatch> batch_;

  friend class Client;
  friend class RecordBatchBaseBuilder;
};

class Table : public BareRegistered<Table>, public Collection<RecordBatch> {
 public:
  static std::unique_ptr<Object> Create() __attribute__((used)) {
    return std::static_pointer_cast<Object>(
        std::unique_ptr<Table>{new Table()});
  }

  void Construct(const ObjectMeta& meta) override;

  void PostConstruct(const ObjectMeta& meta) override;

  std::shared_ptr<arrow::Table> GetTable() const;

  std::shared_ptr<arrow::ChunkedArray> column(int i) const {
    return GetTable()->column(i);
  }

  std::shared_ptr<arrow::Field> field(int i) const {
    return schema_->GetSchema()->field(i);
  }

  std::shared_ptr<arrow::Schema> schema() const { return schema_->GetSchema(); }

  size_t batch_num() const { return batch_num_; }

  size_t num_rows() const { return num_rows_; }

  size_t num_columns() const { return num_columns_; }

  std::vector<std::shared_ptr<RecordBatch>> const& batches() const {
    return batches_;
  }

 private:
  size_t batch_num_, num_rows_, num_columns_;
  Tuple<std::shared_ptr<RecordBatch>> batches_;
  std::shared_ptr<SchemaProxy> schema_;

  mutable std::vector<std::shared_ptr<arrow::RecordBatch>> arrow_batches_;
  mutable std::shared_ptr<arrow::Table> table_;

  friend class Client;
  friend class TableBuilder;
};

template <>
struct collection_type<RecordBatch> {
  using type = Table;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_ARROW_VINEYARD_MOD_

// vim: syntax=cpp

namespace vineyard {

template<typename T>
class NumericArrayBaseBuilder: public ObjectBuilder {
  public:
    // using ArrayType
    using ArrayType = ArrowArrayType<T>;

    explicit NumericArrayBaseBuilder(Client &client) {}

    explicit NumericArrayBaseBuilder(
            NumericArray<T> const &__value) {
        this->set_length_(__value.length_);
        this->set_null_count_(__value.null_count_);
        this->set_offset_(__value.offset_);
        this->set_buffer_(__value.buffer_);
        this->set_null_bitmap_(__value.null_bitmap_);
    }

    explicit NumericArrayBaseBuilder(
            std::shared_ptr<NumericArray<T>> const & __value):
        NumericArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<NumericArray<T>> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<NumericArray<T>>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<NumericArray<T>>());

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->null_count_ = null_count_;
        __value->meta_.AddKeyValue("null_count_", __value->null_count_);

        __value->offset_ = offset_;
        __value->meta_.AddKeyValue("offset_", __value->offset_);

        // using __buffer__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer__value_type = typename decltype(__value->buffer_)::element_type;
        auto __value_buffer_ = std::dynamic_pointer_cast<__buffer__value_type>(
            buffer_->_Seal(client));
        __value->buffer_ = __value_buffer_;
        __value->meta_.AddMember("buffer_", __value->buffer_);
        __value_nbytes += __value_buffer_->nbytes();

        // using __null_bitmap__value_type = typename std::shared_ptr<Blob>::element_type;
        using __null_bitmap__value_type = typename decltype(__value->null_bitmap_)::element_type;
        auto __value_null_bitmap_ = std::dynamic_pointer_cast<__null_bitmap__value_type>(
            null_bitmap_->_Seal(client));
        __value->null_bitmap_ = __value_null_bitmap_;
        __value->meta_.AddMember("null_bitmap_", __value->null_bitmap_);
        __value_nbytes += __value_null_bitmap_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t length_;
    int64_t null_count_;
    int64_t offset_;
    std::shared_ptr<ObjectBase> buffer_;
    std::shared_ptr<ObjectBase> null_bitmap_;

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

    void set_null_count_(int64_t const &null_count__) {
        this->null_count_ = null_count__;
    }

    void set_offset_(int64_t const &offset__) {
        this->offset_ = offset__;
    }

    void set_buffer_(std::shared_ptr<ObjectBase> const & buffer__) {
        this->buffer_ = buffer__;
    }

    void set_null_bitmap_(std::shared_ptr<ObjectBase> const & null_bitmap__) {
        this->null_bitmap_ = null_bitmap__;
    }

  private:
    friend class NumericArray<T>;
};


}  // namespace vineyard




namespace vineyard {


class BooleanArrayBaseBuilder: public ObjectBuilder {
  public:
    // using ArrayType
    using ArrayType = ArrowArrayType<bool>;

    explicit BooleanArrayBaseBuilder(Client &client) {}

    explicit BooleanArrayBaseBuilder(
            BooleanArray const &__value) {
        this->set_length_(__value.length_);
        this->set_null_count_(__value.null_count_);
        this->set_offset_(__value.offset_);
        this->set_buffer_(__value.buffer_);
        this->set_null_bitmap_(__value.null_bitmap_);
    }

    explicit BooleanArrayBaseBuilder(
            std::shared_ptr<BooleanArray> const & __value):
        BooleanArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<BooleanArray> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<BooleanArray>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<BooleanArray>());

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->null_count_ = null_count_;
        __value->meta_.AddKeyValue("null_count_", __value->null_count_);

        __value->offset_ = offset_;
        __value->meta_.AddKeyValue("offset_", __value->offset_);

        // using __buffer__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer__value_type = typename decltype(__value->buffer_)::element_type;
        auto __value_buffer_ = std::dynamic_pointer_cast<__buffer__value_type>(
            buffer_->_Seal(client));
        __value->buffer_ = __value_buffer_;
        __value->meta_.AddMember("buffer_", __value->buffer_);
        __value_nbytes += __value_buffer_->nbytes();

        // using __null_bitmap__value_type = typename std::shared_ptr<Blob>::element_type;
        using __null_bitmap__value_type = typename decltype(__value->null_bitmap_)::element_type;
        auto __value_null_bitmap_ = std::dynamic_pointer_cast<__null_bitmap__value_type>(
            null_bitmap_->_Seal(client));
        __value->null_bitmap_ = __value_null_bitmap_;
        __value->meta_.AddMember("null_bitmap_", __value->null_bitmap_);
        __value_nbytes += __value_null_bitmap_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t length_;
    int64_t null_count_;
    int64_t offset_;
    std::shared_ptr<ObjectBase> buffer_;
    std::shared_ptr<ObjectBase> null_bitmap_;

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

    void set_null_count_(int64_t const &null_count__) {
        this->null_count_ = null_count__;
    }

    void set_offset_(int64_t const &offset__) {
        this->offset_ = offset__;
    }

    void set_buffer_(std::shared_ptr<ObjectBase> const & buffer__) {
        this->buffer_ = buffer__;
    }

    void set_null_bitmap_(std::shared_ptr<ObjectBase> const & null_bitmap__) {
        this->null_bitmap_ = null_bitmap__;
    }

  private:
    friend class BooleanArray;
};


}  // namespace vineyard




namespace vineyard {

template<typename ArrayType>
class BaseBinaryArrayBaseBuilder: public ObjectBuilder {
  public:
    

    explicit BaseBinaryArrayBaseBuilder(Client &client) {}

    explicit BaseBinaryArrayBaseBuilder(
            BaseBinaryArray<ArrayType> const &__value) {
        this->set_length_(__value.length_);
        this->set_null_count_(__value.null_count_);
        this->set_offset_(__value.offset_);
        this->set_buffer_data_(__value.buffer_data_);
        this->set_buffer_offsets_(__value.buffer_offsets_);
        this->set_null_bitmap_(__value.null_bitmap_);
    }

    explicit BaseBinaryArrayBaseBuilder(
            std::shared_ptr<BaseBinaryArray<ArrayType>> const & __value):
        BaseBinaryArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<BaseBinaryArray<ArrayType>> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<BaseBinaryArray<ArrayType>>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<BaseBinaryArray<ArrayType>>());

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->null_count_ = null_count_;
        __value->meta_.AddKeyValue("null_count_", __value->null_count_);

        __value->offset_ = offset_;
        __value->meta_.AddKeyValue("offset_", __value->offset_);

        // using __buffer_data__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer_data__value_type = typename decltype(__value->buffer_data_)::element_type;
        auto __value_buffer_data_ = std::dynamic_pointer_cast<__buffer_data__value_type>(
            buffer_data_->_Seal(client));
        __value->buffer_data_ = __value_buffer_data_;
        __value->meta_.AddMember("buffer_data_", __value->buffer_data_);
        __value_nbytes += __value_buffer_data_->nbytes();

        // using __buffer_offsets__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer_offsets__value_type = typename decltype(__value->buffer_offsets_)::element_type;
        auto __value_buffer_offsets_ = std::dynamic_pointer_cast<__buffer_offsets__value_type>(
            buffer_offsets_->_Seal(client));
        __value->buffer_offsets_ = __value_buffer_offsets_;
        __value->meta_.AddMember("buffer_offsets_", __value->buffer_offsets_);
        __value_nbytes += __value_buffer_offsets_->nbytes();

        // using __null_bitmap__value_type = typename std::shared_ptr<Blob>::element_type;
        using __null_bitmap__value_type = typename decltype(__value->null_bitmap_)::element_type;
        auto __value_null_bitmap_ = std::dynamic_pointer_cast<__null_bitmap__value_type>(
            null_bitmap_->_Seal(client));
        __value->null_bitmap_ = __value_null_bitmap_;
        __value->meta_.AddMember("null_bitmap_", __value->null_bitmap_);
        __value_nbytes += __value_null_bitmap_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t length_;
    int64_t null_count_;
    int64_t offset_;
    std::shared_ptr<ObjectBase> buffer_data_;
    std::shared_ptr<ObjectBase> buffer_offsets_;
    std::shared_ptr<ObjectBase> null_bitmap_;

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

    void set_null_count_(int64_t const &null_count__) {
        this->null_count_ = null_count__;
    }

    void set_offset_(int64_t const &offset__) {
        this->offset_ = offset__;
    }

    void set_buffer_data_(std::shared_ptr<ObjectBase> const & buffer_data__) {
        this->buffer_data_ = buffer_data__;
    }

    void set_buffer_offsets_(std::shared_ptr<ObjectBase> const & buffer_offsets__) {
        this->buffer_offsets_ = buffer_offsets__;
    }

    void set_null_bitmap_(std::shared_ptr<ObjectBase> const & null_bitmap__) {
        this->null_bitmap_ = null_bitmap__;
    }

  private:
    friend class BaseBinaryArray<ArrayType>;
};


}  // namespace vineyard




namespace vineyard {


class FixedSizeBinaryArrayBaseBuilder: public ObjectBuilder {
  public:
    

    explicit FixedSizeBinaryArrayBaseBuilder(Client &client) {}

    explicit FixedSizeBinaryArrayBaseBuilder(
            FixedSizeBinaryArray const &__value) {
        this->set_byte_width_(__value.byte_width_);
        this->set_length_(__value.length_);
        this->set_null_count_(__value.null_count_);
        this->set_offset_(__value.offset_);
        this->set_buffer_(__value.buffer_);
        this->set_null_bitmap_(__value.null_bitmap_);
    }

    explicit FixedSizeBinaryArrayBaseBuilder(
            std::shared_ptr<FixedSizeBinaryArray> const & __value):
        FixedSizeBinaryArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<FixedSizeBinaryArray> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<FixedSizeBinaryArray>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<FixedSizeBinaryArray>());

        __value->byte_width_ = byte_width_;
        __value->meta_.AddKeyValue("byte_width_", __value->byte_width_);

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->null_count_ = null_count_;
        __value->meta_.AddKeyValue("null_count_", __value->null_count_);

        __value->offset_ = offset_;
        __value->meta_.AddKeyValue("offset_", __value->offset_);

        // using __buffer__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer__value_type = typename decltype(__value->buffer_)::element_type;
        auto __value_buffer_ = std::dynamic_pointer_cast<__buffer__value_type>(
            buffer_->_Seal(client));
        __value->buffer_ = __value_buffer_;
        __value->meta_.AddMember("buffer_", __value->buffer_);
        __value_nbytes += __value_buffer_->nbytes();

        // using __null_bitmap__value_type = typename std::shared_ptr<Blob>::element_type;
        using __null_bitmap__value_type = typename decltype(__value->null_bitmap_)::element_type;
        auto __value_null_bitmap_ = std::dynamic_pointer_cast<__null_bitmap__value_type>(
            null_bitmap_->_Seal(client));
        __value->null_bitmap_ = __value_null_bitmap_;
        __value->meta_.AddMember("null_bitmap_", __value->null_bitmap_);
        __value_nbytes += __value_null_bitmap_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    int32_t byte_width_;
    size_t length_;
    int64_t null_count_;
    int64_t offset_;
    std::shared_ptr<ObjectBase> buffer_;
    std::shared_ptr<ObjectBase> null_bitmap_;

    void set_byte_width_(int32_t const &byte_width__) {
        this->byte_width_ = byte_width__;
    }

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

    void set_null_count_(int64_t const &null_count__) {
        this->null_count_ = null_count__;
    }

    void set_offset_(int64_t const &offset__) {
        this->offset_ = offset__;
    }

    void set_buffer_(std::shared_ptr<ObjectBase> const & buffer__) {
        this->buffer_ = buffer__;
    }

    void set_null_bitmap_(std::shared_ptr<ObjectBase> const & null_bitmap__) {
        this->null_bitmap_ = null_bitmap__;
    }

  private:
    friend class FixedSizeBinaryArray;
};


}  // namespace vineyard




namespace vineyard {


class NullArrayBaseBuilder: public ObjectBuilder {
  public:
    // using ArrayType
    using ArrayType = arrow::NullArray;

    explicit NullArrayBaseBuilder(Client &client) {}

    explicit NullArrayBaseBuilder(
            NullArray const &__value) {
        this->set_length_(__value.length_);
    }

    explicit NullArrayBaseBuilder(
            std::shared_ptr<NullArray> const & __value):
        NullArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<NullArray> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<NullArray>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<NullArray>());

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t length_;

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

  private:
    friend class NullArray;
};


}  // namespace vineyard




namespace vineyard {

template<typename ArrayType>
class BaseListArrayBaseBuilder: public ObjectBuilder {
  public:
    

    explicit BaseListArrayBaseBuilder(Client &client) {}

    explicit BaseListArrayBaseBuilder(
            BaseListArray<ArrayType> const &__value) {
        this->set_length_(__value.length_);
        this->set_null_count_(__value.null_count_);
        this->set_offset_(__value.offset_);
        this->set_buffer_offsets_(__value.buffer_offsets_);
        this->set_null_bitmap_(__value.null_bitmap_);
        this->set_values_(__value.values_);
    }

    explicit BaseListArrayBaseBuilder(
            std::shared_ptr<BaseListArray<ArrayType>> const & __value):
        BaseListArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<BaseListArray<ArrayType>> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<BaseListArray<ArrayType>>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<BaseListArray<ArrayType>>());

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->null_count_ = null_count_;
        __value->meta_.AddKeyValue("null_count_", __value->null_count_);

        __value->offset_ = offset_;
        __value->meta_.AddKeyValue("offset_", __value->offset_);

        // using __buffer_offsets__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer_offsets__value_type = typename decltype(__value->buffer_offsets_)::element_type;
        auto __value_buffer_offsets_ = std::dynamic_pointer_cast<__buffer_offsets__value_type>(
            buffer_offsets_->_Seal(client));
        __value->buffer_offsets_ = __value_buffer_offsets_;
        __value->meta_.AddMember("buffer_offsets_", __value->buffer_offsets_);
        __value_nbytes += __value_buffer_offsets_->nbytes();

        // using __null_bitmap__value_type = typename std::shared_ptr<Blob>::element_type;
        using __null_bitmap__value_type = typename decltype(__value->null_bitmap_)::element_type;
        auto __value_null_bitmap_ = std::dynamic_pointer_cast<__null_bitmap__value_type>(
            null_bitmap_->_Seal(client));
        __value->null_bitmap_ = __value_null_bitmap_;
        __value->meta_.AddMember("null_bitmap_", __value->null_bitmap_);
        __value_nbytes += __value_null_bitmap_->nbytes();

        // using __values__value_type = typename std::shared_ptr<Object>::element_type;
        using __values__value_type = typename decltype(__value->values_)::element_type;
        auto __value_values_ = std::dynamic_pointer_cast<__values__value_type>(
            values_->_Seal(client));
        __value->values_ = __value_values_;
        __value->meta_.AddMember("values_", __value->values_);
        __value_nbytes += __value_values_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t length_;
    int64_t null_count_;
    int64_t offset_;
    std::shared_ptr<ObjectBase> buffer_offsets_;
    std::shared_ptr<ObjectBase> null_bitmap_;
    std::shared_ptr<ObjectBase> values_;

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

    void set_null_count_(int64_t const &null_count__) {
        this->null_count_ = null_count__;
    }

    void set_offset_(int64_t const &offset__) {
        this->offset_ = offset__;
    }

    void set_buffer_offsets_(std::shared_ptr<ObjectBase> const & buffer_offsets__) {
        this->buffer_offsets_ = buffer_offsets__;
    }

    void set_null_bitmap_(std::shared_ptr<ObjectBase> const & null_bitmap__) {
        this->null_bitmap_ = null_bitmap__;
    }

    void set_values_(std::shared_ptr<ObjectBase> const & values__) {
        this->values_ = values__;
    }

  private:
    friend class BaseListArray<ArrayType>;
};


}  // namespace vineyard




namespace vineyard {


class FixedSizeListArrayBaseBuilder: public ObjectBuilder {
  public:
    

    explicit FixedSizeListArrayBaseBuilder(Client &client) {}

    explicit FixedSizeListArrayBaseBuilder(
            FixedSizeListArray const &__value) {
        this->set_length_(__value.length_);
        this->set_list_size_(__value.list_size_);
        this->set_values_(__value.values_);
    }

    explicit FixedSizeListArrayBaseBuilder(
            std::shared_ptr<FixedSizeListArray> const & __value):
        FixedSizeListArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<FixedSizeListArray> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<FixedSizeListArray>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<FixedSizeListArray>());

        __value->length_ = length_;
        __value->meta_.AddKeyValue("length_", __value->length_);

        __value->list_size_ = list_size_;
        __value->meta_.AddKeyValue("list_size_", __value->list_size_);

        // using __values__value_type = typename std::shared_ptr<Object>::element_type;
        using __values__value_type = typename decltype(__value->values_)::element_type;
        auto __value_values_ = std::dynamic_pointer_cast<__values__value_type>(
            values_->_Seal(client));
        __value->values_ = __value_values_;
        __value->meta_.AddMember("values_", __value->values_);
        __value_nbytes += __value_values_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t length_;
    size_t list_size_;
    std::shared_ptr<ObjectBase> values_;

    void set_length_(size_t const &length__) {
        this->length_ = length__;
    }

    void set_list_size_(size_t const &list_size__) {
        this->list_size_ = list_size__;
    }

    void set_values_(std::shared_ptr<ObjectBase> const & values__) {
        this->values_ = values__;
    }

  private:
    friend class FixedSizeListArray;
};


}  // namespace vineyard




namespace vineyard {


class SchemaProxyBaseBuilder: public ObjectBuilder {
  public:
    

    explicit SchemaProxyBaseBuilder(Client &client) {}

    explicit SchemaProxyBaseBuilder(
            SchemaProxy const &__value) {
        this->set_schema_textual_(__value.schema_textual_);
        this->set_schema_binary_(__value.schema_binary_);
    }

    explicit SchemaProxyBaseBuilder(
            std::shared_ptr<SchemaProxy> const & __value):
        SchemaProxyBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<SchemaProxy> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<SchemaProxy>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<SchemaProxy>());

        __value->schema_textual_ = schema_textual_;
        __value->meta_.AddKeyValue("schema_textual_", __value->schema_textual_);

        __value->schema_binary_ = schema_binary_;
        __value->meta_.AddKeyValue("schema_binary_", __value->schema_binary_);

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    json schema_textual_;
    json schema_binary_;

    void set_schema_textual_(json const &schema_textual__) {
        this->schema_textual_ = schema_textual__;
    }

    void set_schema_binary_(json const &schema_binary__) {
        this->schema_binary_ = schema_binary__;
    }

  private:
    friend class SchemaProxy;
};


}  // namespace vineyard




namespace vineyard {


class RecordBatchBaseBuilder: public ObjectBuilder {
  public:
    

    explicit RecordBatchBaseBuilder(Client &client) {}

    explicit RecordBatchBaseBuilder(
            RecordBatch const &__value) {
        this->set_column_num_(__value.column_num_);
        this->set_row_num_(__value.row_num_);
        this->set_schema_(
            std::make_shared<typename std::decay<decltype(__value.schema_)>::type>(
                __value.schema_));
        for (auto const &__columns__item: __value.columns_) {
            this->add_columns_(__columns__item);
        }
    }

    explicit RecordBatchBaseBuilder(
            std::shared_ptr<RecordBatch> const & __value):
        RecordBatchBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<RecordBatch> &__value) {
        return __value->meta_;
    }

    Status _Seal(Client& client, std::shared_ptr<Object>& object) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        RETURN_ON_ERROR(this->Build(client));
        auto __value = std::make_shared<RecordBatch>();
        object = __value;

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<RecordBatch>());

        __value->column_num_ = column_num_;
        __value->meta_.AddKeyValue("column_num_", __value->column_num_);

        __value->row_num_ = row_num_;
        __value->meta_.AddKeyValue("row_num_", __value->row_num_);

        // using __schema__value_type = typename SchemaProxy;
        using __schema__value_type = decltype(__value->schema_);
        auto __value_schema_ = std::dynamic_pointer_cast<__schema__value_type>(
            schema_->_Seal(client));
        __value->schema_ = *__value_schema_;
        __value->meta_.AddMember("schema_", __value->schema_);
        __value_nbytes += __value_schema_->nbytes();

        // using __columns__value_type = typename Tuple<std::shared_ptr<Object>>::value_type::element_type;
        using __columns__value_type = typename decltype(__value->columns_)::value_type::element_type;

        size_t __columns__idx = 0;
        for (auto &__columns__value: columns_) {
            auto __value_columns_ = std::dynamic_pointer_cast<__columns__value_type>(
                __columns__value->_Seal(client));
            __value->columns_.emplace_back(__value_columns_);
            __value->meta_.AddMember("__columns_-" + std::to_string(__columns__idx),
                                     __value_columns_);
            __value_nbytes += __value_columns_->nbytes();
            __columns__idx += 1;
        }
        __value->meta_.AddKeyValue("__columns_-size", __value->columns_.size());

        __value->meta_.SetNBytes(__value_nbytes);

        RETURN_ON_ERROR(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return Status::OK();
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t column_num_;
    size_t row_num_;
    std::shared_ptr<ObjectBase> schema_;
    std::vector<std::shared_ptr<ObjectBase>> columns_;

    void set_column_num_(size_t const &column_num__) {
        this->column_num_ = column_num__;
    }

    void set_row_num_(size_t const &row_num__) {
        this->row_num_ = row_num__;
    }

    void set_schema_(std::shared_ptr<ObjectBase> const & schema__) {
        this->schema_ = schema__;
    }

    void set_columns_(std::vector<std::shared_ptr<ObjectBase>> const &columns__) {
        this->columns_ = columns__;
    }
    void set_columns_(size_t const idx, std::shared_ptr<ObjectBase> const &columns__) {
        if (idx >= this->columns_.size()) {
            this->columns_.resize(idx + 1);
        }
        this->columns_[idx] = columns__;
    }
    void add_columns_(std::shared_ptr<ObjectBase> const &columns__) {
        this->columns_.emplace_back(columns__);
    }
    void remove_columns_(const size_t columns__index_) {
        this->columns_.erase(this->columns_.begin() + columns__index_);
    }

  private:
    friend class RecordBatch;
};


}  // namespace vineyard




namespace vineyard {


using RecordBatchStreamBase = vineyard::Stream<RecordBatch>;


}  // namespace vineyard



#endif // MODULES_BASIC_DS_ARROW_VINEYARD_H
